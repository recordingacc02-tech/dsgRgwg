"""Build an SQLite database from the same schema as the MySQL tuition script.
Run: python3 build_sqlite.py
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "tution.db")
if os.path.exists(DB):
    os.remove(DB)

con = sqlite3.connect(DB)
cur = con.cursor()

cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE students (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    phone      TEXT,
    grade      TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teachers (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    subject    TEXT,
    hourly_rate REAL DEFAULT 0.00,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    subject     TEXT,
    teacher_id  INTEGER,
    fee         REAL DEFAULT 0.00,
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
);

CREATE TABLE enrollments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  INTEGER NOT NULL,
    course_id   INTEGER NOT NULL,
    enrolled_at TEXT DEFAULT CURRENT_TIMESTAMP,
    status      TEXT DEFAULT 'active',
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id)  REFERENCES courses(id)  ON DELETE CASCADE,
    UNIQUE(student_id, course_id)
);

CREATE TABLE payments (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_id INTEGER NOT NULL,
    amount        REAL NOT NULL,
    paid_at       TEXT DEFAULT CURRENT_TIMESTAMP,
    method        TEXT DEFAULT 'cash',
    notes         TEXT,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE
);

CREATE INDEX idx_enroll_student ON enrollments(student_id);
CREATE INDEX idx_enroll_course ON enrollments(course_id);
CREATE INDEX idx_pay_enroll ON payments(enrollment_id);
""")

cur.executemany(
    "INSERT INTO teachers (id,name,email,subject,hourly_rate) VALUES (?,?,?,?,?)",
    [(1,'Alice Chen','alice@tution.com','Mathematics',25.00),
     (2,'Brian Smith','brian@tution.com','Physics',30.00),
     (3,'Carla Diaz','carla@tution.com','Chemistry',28.00),
     (4,'David Kumar','david@tution.com','English',22.00)])

cur.executemany(
    "INSERT INTO courses (id,name,subject,teacher_id,fee) VALUES (?,?,?,?,?)",
    [(1,'Algebra 101','Mathematics',1,300.00),
     (2,'Physics Basics','Physics',2,350.00),
     (3,'Organic Chemistry','Chemistry',3,320.00),
     (4,'Essay Writing','English',4,250.00)])

cur.executemany(
    "INSERT INTO students (id,name,email,phone,grade) VALUES (?,?,?,?,?)",
    [(1,'John Doe','john@tution.com','555-0101','10th'),
     (2,'Jane Roe','jane@tution.com','555-0102','11th'),
     (3,'Sam Lee','sam@tution.com','555-0103','9th'),
     (4,'Priya Patel','priya@tution.com','555-0104','12th')])

cur.executemany(
    "INSERT INTO enrollments (id,student_id,course_id,status) VALUES (?,?,?,?)",
    [(1,1,1,'active'),(2,2,2,'active'),(3,3,3,'completed'),
     (4,4,4,'active'),(5,1,3,'active')])

cur.executemany(
    "INSERT INTO payments (id,enrollment_id,amount,method,notes) VALUES (?,?,?,?,?)",
    [(1,1,300.00,'online','Full fee'),
     (2,2,350.00,'card','First installment'),
     (3,3,320.00,'cash','Paid in full'),
     (4,4,250.00,'cheque','Cheque #1023'),
     (5,5,320.00,'online','Partial')])

con.commit()

for t in ("students","teachers","courses","enrollments","payments"):
    print(t, cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])

con.close()
print("SQLite DB written to:", DB)