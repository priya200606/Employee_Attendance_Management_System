import sqlite3

def add_employee():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    name = input("Enter Employee Name: ")
    department = input("Enter Department: ")
    mobile = input("Enter Mobile Number: ")

    cursor.execute(
        "INSERT INTO employee(name, department, mobile) VALUES (?, ?, ?)",
        (name, department, mobile)
    )

    conn.commit()
    conn.close()

    print("Employee Added Successfully")


def search_employee():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    emp_id = input("Enter Employee ID: ")

    cursor.execute("SELECT * FROM employee WHERE id=?", (emp_id,))
    employee = cursor.fetchone()

    if employee:
        print("\nEmployee Found")
        print("ID:", employee[0])
        print("Name:", employee[1])
        print("Department:", employee[2])
        print("Mobile:", employee[3])
    else:
        print("Employee Not Found")

    conn.close()