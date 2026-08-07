from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

# ---------------- CREATE ATTENDANCE TABLE ----------------

def create_attendance_table():

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id TEXT,

        date TEXT,

        status TEXT

    )
    """)

    conn.commit()
    conn.close()



create_attendance_table()

# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ADMIN LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            return render_template("dashboard.html")

        else:
            return """
            <h2 style='color:red;text-align:center;'>
            Invalid Username or Password
            </h2>

            <center>
            <a href='/login'>Try Again</a>
            </center>
            """


    return render_template("login.html")



# ---------------- ADD EMPLOYEE ----------------

@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        employee_id = request.form["employee_id"]
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        mobile = request.form["mobile"]


        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO employee
        (employee_id, name, email, department, mobile)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            employee_id,
            name,
            email,
            department,
            mobile
        ))


        conn.commit()
        conn.close()


        return """
        <h2 style='color:green;text-align:center;'>
        Employee Added Successfully
        </h2>

        <center>

        <a href='/add_employee'>
        Add Another Employee
        </a>

        <br><br>

        <a href='/view_employees'>
        View Employees
        </a>

        </center>
        """


    return render_template("add_employee.html")





# ---------------- VIEW EMPLOYEES ----------------


@app.route("/view_employees")
def view_employees():

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()


    cursor.execute("""
    SELECT rowid,
           employee_id,
           name,
           email,
           department,
           mobile
    FROM employee
    """)


    employees = cursor.fetchall()


    conn.close()


    return render_template(
        "view_employees.html",
        employees=employees
    )





# ---------------- EDIT EMPLOYEE ----------------


@app.route("/edit_employee/<int:id>", methods=["GET", "POST"])
def edit_employee(id):


    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()



    if request.method == "POST":


        employee_id = request.form["employee_id"]
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        mobile = request.form["mobile"]



        cursor.execute("""
        UPDATE employee

        SET employee_id=?,
            name=?,
            email=?,
            department=?,
            mobile=?

        WHERE rowid=?

        """,
        (
            employee_id,
            name,
            email,
            department,
            mobile,
            id
        ))


        conn.commit()
        conn.close()


        return redirect("/view_employees")



    cursor.execute("""
    SELECT rowid,
           employee_id,
           name,
           email,
           department,
           mobile

    FROM employee

    WHERE rowid=?

    """,
    (id,))


    employee = cursor.fetchone()


    conn.close()


    return render_template(
        "edit_employee.html",
        employee=employee
    )





# ---------------- DELETE EMPLOYEE ----------------

@app.route("/delete_employee/<int:id>")
def delete_employee(id):


    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()


    cursor.execute("""
    DELETE FROM employee
    WHERE rowid=?
    """,
    (id,))


    conn.commit()
    conn.close()


    return redirect("/view_employees")

# ---------------- MARK ATTENDANCE ----------------

@app.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance():

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        date TEXT,
        status TEXT
    )
    """)

    if request.method == "POST":

        employee_id = request.form["employee_id"]
        attendance_date = request.form["date"]
        status = request.form["status"]

        cursor.execute("""
        INSERT INTO attendance(employee_id, date, status)
        VALUES (?, ?, ?)
        """,
        (employee_id, attendance_date, status))

        conn.commit()
        conn.close()

        return """
        <h2 style='color:green;text-align:center;'>
        Attendance Saved Successfully
        </h2>

        <center>

        <a href='/mark_attendance'>
        Mark Another Attendance
        </a>

        <br><br>

        <a href='/attendance_report'>
        Attendance Report
        </a>

        </center>
        """

    cursor.execute("""
    SELECT employee_id, name
    FROM employee
    """)

    employees = cursor.fetchall()

    conn.close()

    return render_template(
        "mark_attendance.html",
        employees=employees
    )

# ---------------- ATTENDANCE REPORT ----------------

@app.route("/attendance_report")
def attendance_report():

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT employee_id, date, status
    FROM attendance
    ORDER BY date DESC
    """)

    attendance = cursor.fetchall()

    conn.close()

    return render_template(
        "attendance_report.html",
        attendance=attendance
    )

# ---------------- SEARCH EMPLOYEE ----------------

@app.route("/search_employee", methods=["GET", "POST"])
def search_employee():

    employee = None

    if request.method == "POST":

        employee_id = request.form["employee_id"]

        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT employee_id,
               name,
               email,
               department,
               mobile
        FROM employee
        WHERE employee_id=?
        """, (employee_id,))

        employee = cursor.fetchone()

        conn.close()

    return render_template(
        "search_employee.html",
        employee=employee
    )

# ---------------- RUN SERVER ----------------


if __name__ == "__main__":

    app.run(debug=True)