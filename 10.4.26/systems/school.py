"""School Management System - SQLite CLI"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "school.db")

def init():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade TEXT,
        email TEXT UNIQUE);
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject TEXT);
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL);
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        score REAL,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE);
    """)
    con.commit()
    return con

def add_student(con):
    name = input("Name: "); grade = input("Grade: "); email = input("Email: ")
    con.execute("INSERT INTO students (name,grade,email) VALUES (?,?,?)", (name,grade,email))
    con.commit(); 
    print("Student added.")

def add_teacher(con):
    name = input("Name: "); subject = input("Subject: ")
    con.execute("INSERT INTO teachers (name,subject) VALUES (?,?)", (name,subject))
    con.commit(); print("Teacher added.")

def add_course(con):
    name = input("Course name: ")
    for r in con.execute("SELECT id,name FROM teachers"):
        print(r[0], r[1])
    tid = input("Teacher ID (or blank): ")
    tid = tid if tid.strip() else None
    con.execute("INSERT INTO courses (name,teacher_id) VALUES (?,?)", (name,tid))
    con.commit(); print("Course added.")

def add_grade(con):
    sid = input("Student ID: "); cid = input("Course ID: "); score = input("Score: ")
    con.execute("INSERT INTO grades (student_id,course_id,score) VALUES (?,?,?)", (sid,cid,score))
    con.commit(); print("Grade recorded.")

def list_table(con, table, cols):
    rows = con.execute(f"SELECT {cols} FROM {table}").fetchall()
    if not rows: print("(empty)"); return
    for r in rows: print(r)

def main():
    con = init()
    while True:
        print("\n=== SCHOOL MANAGEMENT ===")
        print("1. Add student   2. Add teacher   3. Add course   4. Record grade")
        print("5. List students 6. List teachers 7. List courses 8. List grades")
        print("9. Student report 0. Exit")
        c = input("Choice: ").strip()
        if c == "1": add_student(con)
        elif c == "2": add_teacher(con)
        elif c == "3": add_course(con)
        elif c == "4": add_grade(con)
        elif c == "5": list_table(con, "students", "id,name,grade,email")
        elif c == "6": list_table(con, "teachers", "id,name,subject")
        elif c == "7": list_table(con, "courses", "id,name,teacher_id")
        elif c == "8": list_table(con, "grades", "id,student_id,course_id,score")
        elif c == "9":
            sid = input("Student ID: ")
            rows = con.execute("""
                SELECT c.name, g.score FROM grades g
                JOIN courses c ON c.id = g.course_id
                WHERE g.student_id = ?""", (sid,)).fetchall()
            print("Grades for student", sid, ":", rows if rows else "none")
        elif c == "0": break
    con.close()

if __name__ == "__main__":
    main()