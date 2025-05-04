import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_path="ams.db"):
        # 1) Open the connection you'll actually use everywhere
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        # 2) Immediately ensure ALL tables exist on *this* connection
        self._create_tables()

    def _create_tables(self):
        # Users table (auth)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email           TEXT PRIMARY KEY,
            hashed_password TEXT NOT NULL,
            role            TEXT NOT NULL
                              CHECK(role IN ('student','company','admin'))
        )
        """)

        # Students table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id        TEXT PRIMARY KEY,
            name              TEXT NOT NULL,
            mobile_number     TEXT NOT NULL,
            email             TEXT NOT NULL UNIQUE,
            gpa               REAL CHECK(gpa BETWEEN 0 AND 5),
            specialization    TEXT NOT NULL,
            preferred_locations TEXT NOT NULL,
            skills            TEXT
        )
        """)

        # Applications table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            application_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email   TEXT    NOT NULL,
            opening_id      INTEGER NOT NULL,
            UNIQUE(student_email, opening_id),
            FOREIGN KEY(student_email) REFERENCES students(email),
            FOREIGN KEY(opening_id)    REFERENCES openings(opening_id)
        )
        """)

        # Openings table (remove UNIQUE on company_email to allow multiple openings)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS openings (
            opening_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            company_email   TEXT   NOT NULL,
            opening_name    TEXT   NOT NULL,
            specialization  TEXT   NOT NULL,
            location        TEXT   NOT NULL,
            stipend         REAL   CHECK(stipend > 0),
            deadline        TEXT   NOT NULL,               -- ISO timestamp
            required_skills TEXT,
            required_gpa    REAL   NOT NULL CHECK(required_gpa BETWEEN 0 AND 5) DEFAULT 0,
            priority        TEXT   NOT NULL CHECK(priority IN ('location','gpa')) DEFAULT 'location',
            FOREIGN KEY(company_email) REFERENCES users(email)
        )
        """)

        # Migrate schema: ensure deadline, required_gpa, priority columns exist
        self.cursor.execute("PRAGMA table_info(openings)")
        cols = [r[1] if isinstance(r, tuple) else r["name"] for r in self.cursor.fetchall()]
        if "deadline" not in cols:
            self.cursor.execute("ALTER TABLE openings ADD COLUMN deadline TEXT NOT NULL DEFAULT ''")
        if "required_gpa" not in cols:
            self.cursor.execute("ALTER TABLE openings ADD COLUMN required_gpa REAL NOT NULL DEFAULT 0")
        if "priority" not in cols:
            self.cursor.execute("ALTER TABLE openings ADD COLUMN priority TEXT NOT NULL DEFAULT 'location'")
        self.conn.commit()

        # Access logs
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_logs (
            log_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            email     TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Session logs
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS session_logs (
            session_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            email       TEXT,
            login_time  TIMESTAMP,
            logout_time TIMESTAMP
        )
        """)

        self.conn.commit()

    # --- USER METHODS ---

    def insert_user(self, user: dict):
        """Insert a new user (email, hashed_password, role)."""
        self.cursor.execute(
            "INSERT INTO users (email, hashed_password, role) VALUES (?, ?, ?)",
            (user["email"], user["hashed_password"], user["role"])
        )
        self.conn.commit()

    def get_user(self, email: str):
        """Fetch a user row by email, or return None if not found."""
        try:
            self.cursor.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            )
            return self.cursor.fetchone()
        except sqlite3.OperationalError:
            return None

    def update_password(self, email: str, new_hashed: str):
        """Update only the password for an existing user."""
        self.cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE email = ?",
            (new_hashed, email)
        )
        self.conn.commit()

    # --- OPENING METHODS ---

    def insert_opening(self, data: dict):
        """
        Insert a new apprenticeship opening.
        Expects keys:
          company_email, opening_name, specialization,
          location, stipend, required_skills,
          required_gpa, priority, deadline
        """
        self.cursor.execute(
            """
            INSERT INTO openings (
                company_email, opening_name, specialization,
                location, stipend, required_skills,
                required_gpa, priority, deadline
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["company_email"],
                data["opening_name"],
                data["specialization"],
                data["location"],
                data["stipend"],
                data.get("required_skills", ""),
                data.get("required_gpa", 0),
                data.get("priority", "location"),
                data.get("deadline", ""),
            )
        )
        self.conn.commit()

    def get_openings_by_company(self, company_email: str):
        """Return a list of openings for the given company email."""
        self.cursor.execute(
            "SELECT * FROM openings WHERE company_email = ?",
            (company_email,)
        )
        return self.cursor.fetchall()

    def get_opening_by_id(self, opening_id: int):
        """Fetch exactly one opening row by its ID."""
        self.cursor.execute(
            "SELECT * FROM openings WHERE opening_id = ?",
            (opening_id,)
        )
        return self.cursor.fetchone()

    def get_openings_by_specialization(self, specialization: str):
        """Return a list of openings matching the given specialization."""
        self.cursor.execute(
            "SELECT * FROM openings WHERE specialization = ?",
            (specialization,)
        )
        return self.cursor.fetchall()

    def update_opening(self, opening_id: int, data: dict):
        """
        Update an existing opening by its ID.
        Handles all fields including deadline.
        """
        self.cursor.execute(
            """
            UPDATE openings SET
                opening_name    = ?,
                specialization  = ?,
                location        = ?,
                stipend         = ?,
                required_skills = ?,
                required_gpa    = ?,
                priority        = ?,
                deadline        = ?
            WHERE opening_id = ?
            """,
            (
                data["opening_name"],
                data["specialization"],
                data["location"],
                data["stipend"],
                data.get("required_skills", ""),
                data.get("required_gpa",  0),
                data.get("priority",     "location"),
                data.get("deadline",     ""),
                opening_id,
            )
        )
        self.conn.commit()

    def delete_opening(self, opening_id: int):
        """Remove an opening by its ID."""
        self.cursor.execute(
            "DELETE FROM openings WHERE opening_id = ?",
            (opening_id,)
        )
        self.conn.commit()

    # --- STUDENT METHODS ---

    def insert_student(self, student: dict):
        """
        student keys:
          - student_id        (str)
          - name              (str)
          - mobile_number     (str)
          - email             (str)
          - gpa               (float)
          - specialization    (str)
          - preferred_locations (str, comma-separated)
          - skills            (str)
        """
        self.cursor.execute(
            """
            INSERT INTO students
              (student_id, name, mobile_number, email, gpa,
               specialization, preferred_locations, skills)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student["student_id"],
                student["name"],
                student["mobile_number"],
                student["email"],
                student["gpa"],
                student["specialization"],
                student["preferred_locations"],
                student["skills"],
            )
        )
        self.conn.commit()

    def get_student_by_email(self, email: str):
        """Return the student row or None if not found."""
        self.cursor.execute(
            "SELECT * FROM students WHERE email = ?", (email,)
        )
        return self.cursor.fetchone()

    def update_student(self, email: str, student: dict):
        """
        Update an existing student’s profile by email.
        `student` must contain the same keys as insert_student.
        """
        self.cursor.execute(
            """
            UPDATE students
               SET student_id         = ?,
                   name               = ?,
                   mobile_number      = ?,
                   gpa                = ?,
                   specialization     = ?,
                   preferred_locations= ?,
                   skills             = ?
             WHERE email = ?
            """,
            (
                student["student_id"],
                student["name"],
                student["mobile_number"],
                student["gpa"],
                student["specialization"],
                student["preferred_locations"],
                student["skills"],
                email
            )
        )
        self.conn.commit()

    # --- APPLICATION METHODS ---

    def apply_to_opening(self, student_email: str, opening_id: int) -> bool:
        """Return True if first-time application; False if already applied."""
        try:
            self.cursor.execute(
                "INSERT INTO applications (student_email, opening_id) VALUES (?,?)",
                (student_email, opening_id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def cancel_application(self, student_email: str, opening_id: int):
        self.cursor.execute(
            "DELETE FROM applications WHERE student_email=? AND opening_id=?",
            (student_email, opening_id)
        )
        self.conn.commit()

    def get_applicants_by_opening(self, opening_id: int):
        """Return sqlite3.Rows of students who applied to this opening."""
        self.cursor.execute("""
            SELECT s.*
              FROM students s
              JOIN applications a ON s.email=a.student_email
             WHERE a.opening_id=?
        """, (opening_id,))
        return self.cursor.fetchall()

    def log_access(self, email: str):
        """
        Record a login attempt in the access_logs table.
        Stores the email and current timestamp.
        """
        self.cursor.execute(
            "INSERT INTO access_logs (email) VALUES (?)",
            (email,)
        )
        self.conn.commit()

    def log_session(self, email: str, login: bool):
        """
        If login=True, insert a new session log with login_time.
        If login=False, update the most recent session log (with no logout_time) for this email.
        """
        if login:
            self.cursor.execute(
                "INSERT INTO session_logs (email, login_time) VALUES (?, CURRENT_TIMESTAMP)",
                (email,)
            )
        else:
            self.cursor.execute(
                "UPDATE session_logs SET logout_time = CURRENT_TIMESTAMP \
                 WHERE email = ? AND logout_time IS NULL",
                (email,)
            )
        self.conn.commit()

    def close(self):
        self.conn.close()
