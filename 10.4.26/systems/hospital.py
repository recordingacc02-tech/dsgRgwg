"""Hospital Management System - SQLite CLI"""
import sqlite3, os, datetime

DB = os.path.join(os.path.dirname(__file__), "hospital.db")

def init():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT,
        phone TEXT);
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        phone TEXT);
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER,
        patient_id INTEGER,
        appt_time TEXT,
        status TEXT DEFAULT 'scheduled',
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
        FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE);
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        amount REAL,
        paid INTEGER DEFAULT 0,
        FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE);
    """)
    con.commit()
    return con

def add_doctor(con):
    name = input("Name: "); spec = input("Specialty: "); phone = input("Phone: ")
    con.execute("INSERT INTO doctors (name,specialty,phone) VALUES (?,?,?)",
                (name,spec,phone))
    con.commit(); print("Doctor added.")

def add_patient(con):
    name = input("Name: "); age = input("Age: "); phone = input("Phone: ")
    con.execute("INSERT INTO patients (name,age,phone) VALUES (?,?,?)",
                (name,age,phone))
    con.commit(); print("Patient added.")

def add_appointment(con):
    for r in con.execute("SELECT id,name FROM doctors"): print("D", r[0], r[1])
    for r in con.execute("SELECT id,name FROM patients"): print("P", r[0], r[1])
    did = input("Doctor ID: "); pid = input("Patient ID: ")
    t = input("Time (YYYY-MM-DD HH:MM): ")
    con.execute("INSERT INTO appointments (doctor_id,patient_id,appt_time) VALUES (?,?,?)",
                (did,pid,t))
    con.commit(); print("Appointment booked.")

def add_bill(con):
    pid = input("Patient ID: "); amt = input("Amount: ")
    con.execute("INSERT INTO bills (patient_id,amount) VALUES (?,?)", (pid,amt))
    con.commit(); print("Bill created.")

def list_table(con, q):
    rows = con.execute(q).fetchall()
    if not rows: print("(empty)"); return
    for r in rows: print(r)

def main():
    con = init()
    while True:
        print("\n=== HOSPITAL MANAGEMENT ===")
        print("1. Add doctor   2. Add patient   3. Book appointment   4. Add bill")
        print("5. List doctors 6. List patients 7. List appointments 8. List bills")
        print("9. Mark bill paid  10. Today's appointments  0. Exit")
        c = input("Choice: ").strip()
        if c == "1": add_doctor(con)
        elif c == "2": add_patient(con)
        elif c == "3": add_appointment(con)
        elif c == "4": add_bill(con)
        elif c == "5": list_table(con, "SELECT id,name,specialty,phone FROM doctors")
        elif c == "6": list_table(con, "SELECT id,name,age,phone FROM patients")
        elif c == "7": list_table(con, "SELECT id,doctor_id,patient_id,appt_time,status FROM appointments")
        elif c == "8": list_table(con, "SELECT id,patient_id,amount,paid FROM bills")
        elif c == "9":
            bid = input("Bill ID: ")
            con.execute("UPDATE bills SET paid=1 WHERE id=?", (bid,))
            con.commit(); print("Bill marked paid.")
        elif c == "10":
            today = datetime.date.today().isoformat()
            list_table(con, f"""SELECT a.id, d.name, p.name, a.appt_time
                FROM appointments a
                JOIN doctors d ON d.id=a.doctor_id
                JOIN patients p ON p.id=a.patient_id
                WHERE a.appt_time LIKE '{today}%'""")
        elif c == "0": break
    con.close()

if __name__ == "__main__":
    main()