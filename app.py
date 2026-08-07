from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "employee_management_secret_key"

# ---------------- HOME ----------------

@app.route('/')
def home():
    return render_template('index.html')

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET','POST'])
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



# ---------------- HOME PAGE ----------------

@app.route('/')
def home():
    return render_template('index.html')



# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('attendance.db')
    cur = conn.cursor()

    # Total Employees
    cur.execute("SELECT COUNT(*) FROM employee")
    total_employee = cur.fetchone()[0]


    # Total Attendance
    cur.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cur.fetchone()[0]


    # Present Count
    cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
    present = cur.fetchone()[0]


    # Absent Count
    cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Absent'")
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

@app.route('/add_employee', methods=['GET','POST'])
def add_employee():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        mobile = request.form['mobile']


        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()


        cur.execute("""
        INSERT INTO employee
        (name,email,department,mobile)
        VALUES(?,?,?,?)
        """,
        (name,email,department,mobile))


        conn.commit()
        conn.close()


        return redirect('/view_employees')


    return render_template('add_employee.html')



# ---------------- VIEW EMPLOYEE ----------------

@app.route('/view_employees')
def view_employee():

    conn = sqlite3.connect('employee.db')
    cur = conn.cursor()


    cur.execute("SELECT * FROM employee")

    employees = cur.fetchall()


    conn.close()


    return render_template(
        'view_employees.html',
        employees=employees
    )



# ---------------- EDIT EMPLOYEE ----------------

@app.route('/edit_employee/<int:id>', methods=['GET','POST'])
def edit_employee(id):

    conn = sqlite3.connect('employee.db')
    cur = conn.cursor()


    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        mobile = request.form['mobile']


        cur.execute("""
        UPDATE employee
        SET name=?,
            email=?,
            department=?,
            mobile=?
        WHERE id=?
        """,
        (name,email,department,mobile,id))


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

@app.route('/mark_attendance', methods=['GET','POST'])
def mark_attendance():

    conn = sqlite3.connect('attendance.db')
    cur = conn.cursor()


    if request.method == 'POST':

        employee_id = request.form['employee_id']
        date = request.form['date']
        status = request.form['status']


        cur.execute("""
        INSERT INTO attendance
        (employee_id, date, status)
        VALUES(?,?,?)
        """,
        (employee_id, date, status))


        conn.commit()

        conn.close()


        return redirect('/attendance_report')



    cur.execute("SELECT * FROM employee")

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


    try:

        cur.execute("SELECT * FROM attendance")

        attendance = cur.fetchall()


    except:

        attendance = []


    conn.close()


    return render_template(
        'attendance_report.html',
        attendance=attendance
    )


# ---------------- SEARCH EMPLOYEE ----------------

@app.route('/search_employee', methods=['GET','POST'])
def search_employee():

    employees = []

    if request.method == 'POST':

        employee_id = request.form['employee_id']


        conn = sqlite3.connect('attendance.db')
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

# ---------------- EMPLOYEE LOGIN ----------------

@app.route('/employee_login', methods=['GET','POST'])
def employee_login():

    if request.method == 'POST':

        emp_id = request.form['emp_id']
        password = request.form['password']


        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()


        cursor.execute(
            "SELECT * FROM employee WHERE id=? AND password=?",
            (emp_id,password)
        )


        employee = cursor.fetchone()


        conn.close()


        if employee:

            return redirect('/employee_dashboard')


        else:

            return "Invalid Employee Login"


    return render_template('employee_login.html')



# ---------------- EMPLOYEE DASHBOARD ----------------

@app.route('/employee_dashboard')
def employee_dashboard():

    return render_template('employee_dashboard.html')


# ---------------- DELETE EMPLOYEE ----------------

@app.route('/delete_employee/<int:id>')
def delete_employee(id):

    conn = sqlite3.connect('attendance.db')
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

    return redirect('/login')

# ---------------- RUN APP ----------------

if __name__ == "__main__":

    app.run(debug=True)