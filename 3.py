from flask import Flask, render_template_string, request, redirect, url_for, flash
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'database': 'admission_systemmm'
}

# Admin Dashboard - View all students with options to approve or delete
@app.route('/admin_dashboard')
def admin_dashboard():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT Students.StudentID, Students.FirstName, Students.LastName, Students.Email, 
               Students.Status, Departments.DepartmentName 
        FROM Students 
        JOIN Departments ON Students.DepartmentID = Departments.DepartmentID
    """)
    students = cursor.fetchall()
    cursor.close()
    connection.close()

    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Dashboard</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1 class="mt-4">Student Registrations</h1>
            <table class="table table-bordered mt-4">
                <thead>
                    <tr>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Email</th>
                        <th>Department</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in students %}
                        <tr>
                            <td>{{ student['FirstName'] }}</td>
                            <td>{{ student['LastName'] }}</td>
                            <td>{{ student['Email'] }}</td>
                            <td>{{ student['DepartmentName'] }}</td>
                            <td>{{ student['Status'] }}</td>
                            <td>
                                {% if student['Status'] == 'Pending' %}
                                    <a href="{{ url_for('approve_student', student_id=student['StudentID']) }}" class="btn btn-success btn-sm">Approve</a>
                                {% endif %}
                                <a href="{{ url_for('delete_student', student_id=student['StudentID']) }}" class="btn btn-danger btn-sm">Delete</a>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
            <a href="{{ url_for('start_page') }}" class="btn btn-primary">Back to Home</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_code, students=students)

# Approve student registration
@app.route('/approve_student/<int:student_id>')
def approve_student(student_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE Students SET Status = 'Approved' WHERE StudentID = %s", (student_id,))
        connection.commit()
        flash('Student approved successfully!', 'success')
    except mysql.connector.Error as e:
        connection.rollback()
        flash(f'Error during approval: {e}', 'danger')
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('admin_dashboard'))

# Delete student registration
@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        # Delete the student from the database
        cursor.execute("DELETE FROM Students WHERE StudentID = %s", (student_id,))
        connection.commit()
        flash('Student deleted successfully!', 'success')
    except mysql.connector.Error as e:
        connection.rollback()
        flash(f'Error during deletion: {e}', 'danger')
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('admin_dashboard'))

# Existing routes for start_page, student_registration_page, admin_login_page, register_student, etc.

if __name__ == '__main__':
    app.run(debug=True)
