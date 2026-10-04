"""Library Management System - SQLite CLI"""
import sqlite3, os, datetime

DB = os.path.join(os.path.dirname(__file__), "library.db")

def init():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        isbn TEXT UNIQUE,
        copies INTEGER DEFAULT 1);
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE);
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        member_id INTEGER,
        loan_date TEXT,
        return_date TEXT,
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
        FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE);
    """)
    con.commit()
    return con

def add_book(con):
    title = input("Title: "); author = input("Author: "); isbn = input("ISBN: ")
    copies = input("Copies [1]: ") or "1"
    con.execute("INSERT INTO books (title,author,isbn,copies) VALUES (?,?,?,?)",
                (title,author,isbn,copies))
    con.commit(); print("Book added.")

def add_member(con):
    name = input("Name: "); email = input("Email: ")
    con.execute("INSERT INTO members (name,email) VALUES (?,?)", (name,email))
    con.commit(); print("Member added.")

def borrow(con):
    book_id = input("Book ID: "); member_id = input("Member ID: ")
    copies = con.execute("SELECT copies FROM books WHERE id=?", (book_id,)).fetchone()
    if not copies: print("No such book."); return
    if copies[0] <= 0: print("No copies available."); return
    con.execute("INSERT INTO loans (book_id,member_id,loan_date) VALUES (?,?,?)",
                (book_id, member_id, datetime.date.today().isoformat()))
    con.execute("UPDATE books SET copies = copies - 1 WHERE id=?", (book_id,))
    con.commit(); print("Book borrowed.")

def return_book(con):
    loan_id = input("Loan ID: ")
    loan = con.execute("SELECT book_id FROM loans WHERE id=? AND return_date IS NULL",
                       (loan_id,)).fetchone()
    if not loan: print("No open loan with that ID."); return
    con.execute("UPDATE loans SET return_date=? WHERE id=?",
                (datetime.date.today().isoformat(), loan_id))
    con.execute("UPDATE books SET copies = copies + 1 WHERE id=?", (loan[0],))
    con.commit(); print("Book returned.")

def list_table(con, table, cols):
    rows = con.execute(f"SELECT {cols} FROM {table}").fetchall()
    if not rows: print("(empty)"); return
    for r in rows: print(r)

def main():
    con = init()
    while True:
        print("\n=== LIBRARY MANAGEMENT ===")
        print("1. Add book   2. Add member   3. Borrow   4. Return")
        print("5. List books 6. List members 7. Open loans 8. Search")
        print("0. Exit")
        c = input("Choice: ").strip()
        if c == "1": add_book(con)
        elif c == "2": add_member(con)
        elif c == "3": borrow(con)
        elif c == "4": return_book(con)
        elif c == "5": list_table(con, "books", "id,title,author,copies")
        elif c == "6": list_table(con, "members", "id,name,email")
        elif c == "7": list_table(con, "loans", "id,book_id,member_id,loan_date")
        elif c == "8":
            q = input("Search title/author: ")
            for r in con.execute("SELECT id,title,author,copies FROM books WHERE title LIKE ? OR author LIKE ?",
                                 (f"%{q}%", f"%{q}%")):
                print(r)
        elif c == "0": break
    con.close()

if __name__ == "__main__":
    main()