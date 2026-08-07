import sqlite3

def connect_db():

    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    # Delete old tables
    cursor.execute("DROP TABLE IF EXISTS employee")
    cursor.execute("DROP TABLE IF EXISTS attendance")

    # Employee Table
    cursor.execute("""
    CREATE TABLE employee(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        name TEXT,
        email TEXT,
        department TEXT,
        mobile TEXT
    )
    """)

    # Attendance Table
    cursor.execute("""
    CREATE TABLE attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        date TEXT,
        status TEXT
    )
    """)


    conn.commit()
    conn.close()

    print("Database Created Successfully")

connect_db()