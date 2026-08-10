from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "employee_management_secret_key"


# ---------------- HOME ----------------

@app.route('/')
def home():
    return render_template('index.html')


# ---------------- ADMIN LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "1234":

            session['admin'] = username

            return redirect('/dashboard')

        else:
            return "Invalid Username or Password"

    return render_template('login.html')


# ---------------- EMPLOYEE LOGIN ----------------

@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():

    if request.method == 'POST':

        employee_id = request.form['username']
        password = request.form['password']

        if password == "1234":

            conn = sqlite3.connect('employee.db')
            cur = conn.cursor()

            cur.execute(
                "SELECT employee_id FROM employee WHERE employee_id=?",
                (employee_id,)
            )

            employee = cur.fetchone()

            conn.close()

            if employee:

                session['employee'] = employee_id

                return redirect('/employee_dashboard')

        return "Invalid Employee ID or Password"

    return render_template('employee_login.html')


# ---------------- EMPLOYEE DASHBOARD ----------------

@app.route('/employee_dashboard')
def employee_dashboard():

    employee_id = session.get('employee')

    total_days = 0
    present = 0
    absent = 0
    percentage = 0
    attendance = []

    if employee_id:

        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()

        # Total Attendance
        cur.execute(
            "SELECT COUNT(*) FROM attendance WHERE employee_id=?",
            (employee_id,)
        )

        total_days = cur.fetchone()[0]

        # Present
        cur.execute(
            "SELECT COUNT(*) FROM attendance WHERE employee_id=? AND status='Present'",
            (employee_id,)
        )

        present = cur.fetchone()[0]

        # Absent
        cur.execute(
            "SELECT COUNT(*) FROM attendance WHERE employee_id=? AND status='Absent'",
            (employee_id,)
        )

        absent = cur.fetchone()[0]

        # Attendance Details
        cur.execute(
            "SELECT date, status FROM attendance WHERE employee_id=? ORDER BY date DESC",
            (employee_id,)
        )

        attendance = cur.fetchall()

        conn.close()

        # Percentage
        if total_days > 0:

            percentage = round(
                (present / total_days) * 100,
                2
            )

    return render_template(
        'employee_dashboard.html',
        total_days=total_days,
        present=present,
        absent=absent,
        percentage=percentage,
        attendance=attendance
    )


# ---------------- ADMIN DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('employee.db')
    cur = conn.cursor()

    # Total Employees
    cur.execute(
        "SELECT COUNT(*) FROM employee"
    )

    total_employee = cur.fetchone()[0]

    # Total Attendance
    cur.execute(
        "SELECT COUNT(*) FROM attendance"
    )

    total_attendance = cur.fetchone()[0]

    # Present
    cur.execute(
        "SELECT COUNT(*) FROM attendance WHERE status='Present'"
    )

    present = cur.fetchone()[0]

    # Absent
    cur.execute(
        "SELECT COUNT(*) FROM attendance WHERE status='Absent'"
    )

    absent = cur.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        total_employee=total_employee,
        total_attendance=total_attendance,
        present=present,
        absent=absent
    )


# ---------------- ADD EMPLOYEE ----------------

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():

    if request.method == 'POST':

        employee_id = request.form['employee_id']
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        mobile = request.form['mobile']

        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO employee
            (employee_id, name, email, department, mobile)
            VALUES (?, ?, ?, ?, ?)
        """, (
            employee_id,
            name,
            email,
            department,
            mobile
        ))

        conn.commit()
        conn.close()

        return redirect('/view_employees')

    return render_template('add_employee.html')


# ---------------- VIEW EMPLOYEE ----------------

@app.route('/view_employees')
def view_employee():

    conn = sqlite3.connect('employee.db')
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM employee"
    )

    employees = cur.fetchall()

    conn.close()

    return render_template(
        'view_employees.html',
        employees=employees
    )


# ---------------- EDIT EMPLOYEE ----------------

@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):

    conn = sqlite3.connect('employee.db')
    cur = conn.cursor()

    if request.method == 'POST':

        employee_id = request.form['employee_id']
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        mobile = request.form['mobile']

        cur.execute("""
            UPDATE employee
            SET employee_id=?,
                name=?,
                email=?,
                department=?,
                mobile=?
            WHERE id=?
        """, (
            employee_id,
            name,
            email,
            department,
            mobile,
            id
        ))

        conn.commit()
        conn.close()

        return redirect('/view_employees')

    cur.execute(
        "SELECT * FROM employee WHERE id=?",
        (id,)
    )

    employee = cur.fetchone()

    conn.close()

    return render_template(
        'edit_employee.html',
        employee=employee
    )


# ---------------- MARK ATTENDANCE ----------------

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():

    conn = sqlite3.connect('employee.db')
    cur = conn.cursor()

    if request.method == 'POST':

        employee_id = request.form['employee_id']
        date = request.form['date']
        status = request.form['status']

        cur.execute("""
            INSERT INTO attendance
            (employee_id, date, status)
            VALUES (?, ?, ?)
        """, (
            employee_id,
            date,
            status
        ))

        conn.commit()
        conn.close()

        return redirect('/attendance_report')

    cur.execute(
        "SELECT * FROM employee"
    )

    employees = cur.fetchall()

    conn.close()

    return render_template(
        'mark_attendance.html',
        employees=employees
    )


# ---------------- ATTENDANCE REPORT ----------------

@app.route('/attendance_report')
def attendance_report():

    conn = sqlite3.connect('employee.db')
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM attendance"
    )

    attendance = cur.fetchall()

    conn.close()

    return render_template(
        'attendance_report.html',
        attendance=attendance
    )


# ---------------- SEARCH EMPLOYEE ----------------

@app.route('/search_employee', methods=['GET', 'POST'])
def search_employee():

    employees = []

    if request.method == 'POST':

        employee_id = request.form['employee_id']

        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM employee WHERE employee_id=?",
            (employee_id,)
        )

        employees = cur.fetchall()

        conn.close()

    return render_template(
        'search_employee.html',
        employees=employees
    )


# ---------------- DELETE EMPLOYEE ----------------

@app.route('/delete_employee/<int:id>')
def delete_employee(id):

    conn = sqlite3.connect('employee.db')
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM employee WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/view_employees')


# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():

    session.pop('admin', None)
    session.pop('employee', None)

    return redirect('/login')


# ---------------- RUN APP ----------------

if __name__ == '__main__':

    app.run(debug=True)