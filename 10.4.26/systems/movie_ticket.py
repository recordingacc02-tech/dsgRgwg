"""Movie Ticket Booking System - SQLite CLI"""
import sqlite3, os, datetime

DB = os.path.join(os.path.dirname(__file__), "cinema.db")

def init():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT,
        duration_min INTEGER);
    CREATE TABLE IF NOT EXISTS shows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        show_time TEXT,
        seats_total INTEGER DEFAULT 50,
        FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE);
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        show_id INTEGER,
        customer TEXT,
        seats INTEGER DEFAULT 1,
        booked_at TEXT,
        FOREIGN KEY (show_id) REFERENCES shows(id) ON DELETE CASCADE);
    """)
    con.commit()
    return con

def add_movie(con):
    title = input("Title: "); genre = input("Genre: "); dur = input("Duration (min): ")
    con.execute("INSERT INTO movies (title,genre,duration_min) VALUES (?,?,?)",
                (title,genre,dur))
    con.commit(); print("Movie added.")

def add_show(con):
    for r in con.execute("SELECT id,title FROM movies"):
        print(r[0], r[1])
    mid = input("Movie ID: "); st = input("Show time (YYYY-MM-DD HH:MM): ")
    seats = input("Total seats [50]: ") or "50"
    con.execute("INSERT INTO shows (movie_id,show_time,seats_total) VALUES (?,?,?)",
                (mid,st,seats))
    con.commit(); print("Show added.")

def book(con):
    for r in con.execute("""SELECT s.id, m.title, s.show_time, s.seats_total
                            FROM shows s JOIN movies m ON m.id=s.movie_id"""):
        print(r)
    sid = input("Show ID: "); cust = input("Customer name: ")
    seats = input("Seats [1]: ") or "1"
    taken = con.execute("SELECT COALESCE(SUM(seats),0) FROM bookings WHERE show_id=?",
                        (sid,)).fetchone()[0]
    total = con.execute("SELECT seats_total FROM shows WHERE id=?", (sid,)).fetchone()
    if not total: print("No such show."); return
    if taken + int(seats) > total[0]:
        print("Not enough seats. Available:", total[0] - taken); return
    con.execute("INSERT INTO bookings (show_id,customer,seats,booked_at) VALUES (?,?,?,?)",
                (sid,cust,seats,datetime.datetime.now().isoformat()))
    con.commit(); print("Booked.")

def list_table(con, q):
    rows = con.execute(q).fetchall()
    if not rows: print("(empty)"); return
    for r in rows: print(r)

def main():
    con = init()
    while True:
        print("\n=== MOVIE TICKET BOOKING ===")
        print("1. Add movie  2. Add show  3. Book ticket  4. List movies")
        print("5. List shows 6. List bookings 7. Show availability  0. Exit")
        c = input("Choice: ").strip()
        if c == "1": add_movie(con)
        elif c == "2": add_show(con)
        elif c == "3": book(con)
        elif c == "4": list_table(con, "SELECT id,title,genre,duration_min FROM movies")
        elif c == "5": list_table(con, "SELECT id,movie_id,show_time,seats_total FROM shows")
        elif c == "6": list_table(con, "SELECT id,show_id,customer,seats,booked_at FROM bookings")
        elif c == "7":
            for r in con.execute("""SELECT s.id, m.title, s.show_time,
                s.seats_total - COALESCE(SUM(b.seats),0) AS available
                FROM shows s JOIN movies m ON m.id=s.movie_id
                LEFT JOIN bookings b ON b.show_id=s.id
                GROUP BY s.id"""):
                print(r)
        elif c == "0": break
    con.close()

if __name__ == "__main__":
    main()