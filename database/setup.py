import sqlite3

def create_tables():
    conn = sqlite3.connect("ams.db")
    cursor = conn.cursor()

    # … existing students table …

    # --- OPENINGS TABLE (now with opening_name) ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS openings (
        opening_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        company_email   TEXT NOT NULL,
        opening_name    TEXT NOT NULL,
        specialization  TEXT NOT NULL,
        location        TEXT NOT NULL,
        stipend         REAL CHECK(stipend > 0),
        required_skills TEXT,
        FOREIGN KEY(company_email) REFERENCES users(email)
    )
    """)

    # … existing users, logs, etc. …

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
