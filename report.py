import sqlite3

def view_employees():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()

    print("\n----- Employee List -----")

    for emp in employees:
        print(f"ID: {emp[0]}")
        print(f"Name: {emp[1]}")
        print(f"Department: {emp[2]}")
        print(f"Mobile: {emp[3]}")
        print("-" * 30)

    conn.close()
