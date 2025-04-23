# database/db_manager.py

import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_path="ams.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    # ------------------ STUDENT METHODS ------------------
    def insert_student(self, student):
        query = '''INSERT INTO students (student_id, name, mobile_number, email, gpa, specialization, preferred_locations, skills)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        self.cursor.execute(query, (
            student["student_id"], student["name"], student["mobile_number"],
            student["email"], student["gpa"], student["specialization"],
            ",".join(student["preferred_locations"]), ",".join(student["skills"])
        ))
        self.conn.commit()

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        self.conn.commit()

    def update_student(self, student_id, update_data):
        fields = ", ".join([f"{key} = ?" for key in update_data])
        values = list(update_data.values())
        values.append(student_id)
        query = f"UPDATE students SET {fields} WHERE student_id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    # ------------------ OPENING METHODS ------------------
    def insert_opening(self, opening):
        query = """INSERT INTO openings (company_email, specialization, location, stipend, required_skills)
                   VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(query, (
            opening["company_email"], opening["specialization"], opening["location"],
            opening["stipend"], ",".join(opening["required_skills"])
        ))
        self.conn.commit()

    def delete_opening(self, opening_id):
        self.cursor.execute("DELETE FROM openings WHERE opening_id = ?", (opening_id,))
        self.conn.commit()

    def update_opening(self, opening_id, update_data):
        fields = ", ".join([f"{key} = ?" for key in update_data])
        values = list(update_data.values())
        values.append(opening_id)
        query = f"UPDATE openings SET {fields} WHERE opening_id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_openings(self):
        self.cursor.execute("SELECT * FROM openings")
        return self.cursor.fetchall()

    # ------------------ MATCHING ------------------
    def insert_match(self, student_id, opening_id):
        self.cursor.execute("INSERT INTO matches (student_id, opening_id) VALUES (?, ?)", (student_id, opening_id))
        self.conn.commit()

    def get_matches(self):
        self.cursor.execute("""
        SELECT s.name, s.gpa, o.specialization, o.location, o.stipend
        FROM matches m
        JOIN students s ON m.student_id = s.student_id
        JOIN openings o ON m.opening_id = o.opening_id
        """)
        return self.cursor.fetchall()

    # ------------------ AUTH & LOGGING ------------------
    def add_user(self, email, password_hash, role):
        self.cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", (email, password_hash, role))
        self.conn.commit()

    def get_user(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone()

    def log_access(self, email):
        self.cursor.execute("INSERT INTO access_logs (email) VALUES (?)", (email,))
        self.conn.commit()

    def log_session(self, email, login=True):
        if login:
            self.cursor.execute("INSERT INTO session_logs (email, login_time) VALUES (?, ?)", (email, datetime.now()))
        else:
            self.cursor.execute("UPDATE session_logs SET logout_time = ? WHERE email = ? AND logout_time IS NULL", (datetime.now(), email))
        self.conn.commit()

    def close(self):
        self.conn.close()
