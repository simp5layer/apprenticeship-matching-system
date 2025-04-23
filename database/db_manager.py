# database/setup.py

import sqlite3

def create_tables():
    conn = sqlite3.connect("ams.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        mobile_number TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        gpa REAL CHECK(gpa BETWEEN 0 AND 5),
        specialization TEXT NOT NULL,
        preferred_locations TEXT NOT NULL, -- Comma-separated
        skills TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS openings (
        opening_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_email TEXT NOT NULL,
        specialization TEXT NOT NULL,
        location TEXT NOT NULL,
        stipend REAL CHECK(stipend > 0),
        required_skills TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        opening_id INTEGER NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(opening_id) REFERENCES openings(opening_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('student', 'company', 'admin')) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS access_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS session_logs (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        login_time TIMESTAMP,
        logout_time TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
