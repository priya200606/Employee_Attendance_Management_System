import sqlite3


def connect_db():

    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    # ---------------- EMPLOYEE TABLE ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        name TEXT,
        email TEXT,
        department TEXT,
        mobile TEXT
    )
    """)

    # ---------------- ATTENDANCE TABLE ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        date TEXT,
        status TEXT
    )
    """)

    # ---------------- LEAVE TABLE ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leave_request(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        leave_date TEXT,
        reason TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    conn.commit()
    conn.close()

    print("Database Created Successfully")


connect_db()