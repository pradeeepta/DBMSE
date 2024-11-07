from flask import Flask, render_template_string, request, redirect, url_for, flash
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Configure upload folder for profile images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it does not exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # replace with your database username
    'password': '123456789',  # replace with your database password
    'database': 'admission_systemmm'  # correct database name
}

# Start page with two options
@app.route('/')
def start_page():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container text-center mt-5">
            <h1>Welcome to the Admission System</h1>
            <div class="mt-4">
                <a href="{{ url_for('student_registration_page') }}" class="btn btn-primary btn-lg">Student Registration</a>
                <a href="{{ url_for('admin_login_page') }}" class="btn btn-secondary btn-lg">Admin Login</a>
            </div>
        </div>
    </body>
    </html>
    """)

# Student Registration Page
@app.route('/student_registration')
def student_registration_page():
    # Fetch departments from the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Departments")
    departments = cursor.fetchall()
    cursor.close()
    connection.close()

    # HTML template with Jinja2 syntax for dynamic content rendering
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Admission System</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <header>
            <h1 class="text-center">Student Admission System</h1>
        </header>

        <main class="container">
            <section id="registration">
                <h2>Student Registration</h2>
                <form action="/register_student" method="POST" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="username">Username:</label>
                        <input type="text" id="username" name="username" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password:</label>
                        <input type="password" id="password" name="password" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="first_name">First Name:</label>
                        <input type="text" id="first_name" name="first_name" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="last_name">Last Name:</label>
                        <input type="text" id="last_name" name="last_name" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input type="email" id="email" name="email" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="age">Age:</label>
                        <input type="number" id="age" name="age" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="phone_number">Phone Number:</label>
                        <input type="tel" id="phone_number" name="phone_number" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="marks10th">Marks (10th):</label>
                        <input type="number" step="0.01" id="marks10th" name="marks10th" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="marks12th">Marks (12th):</label>
                        <input type="number" step="0.01" id="marks12th" name="marks12th" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="department_id">Department:</label>
                        <select id="department_id" name="department_id" class="form-control" required>
                            {% for department in departments %}
                                <option value="{{ department['DepartmentID'] }}">{{ department['DepartmentName'] }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="course">Course:</label>
                        <input type="text" id="course" name="course" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="profile_image">Profile Image:</label>
                        <input type="file" id="profile_image" name="profile_image" class="form-control">
                    </div>
                    <button type="submit" class="btn btn-primary">Register</button>
                </form>
            </section>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <div class="mt-4">
                        {% for category, message in messages %}
                            <div class="alert alert-{{ category }}">{{ message }}</div>
                        {% endfor %}
                    </div>
                {% endif %}
            {% endwith %}
        </main>
    </body>
    </html>
    """
    return render_template_string(html_code, departments=departments)


# Admin Login Page
@app.route('/admin_login_page')
def admin_login_page():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Login</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <header>
            <h1 class="text-center">Admin Login</h1>
        </header>
        <main class="container">
            <section id="admin_login">
                <h2>Admin Login</h2>
                <form action="/admin_login" method="POST">
                    <div class="form-group">
                        <label for="admin_username">Username:</label>
                        <input type="text" id="admin_username" name="admin_username" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="admin_password">Password:</label>
                        <input type="password" id="admin_password" name="admin_password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Login</button>
                </form>
            </section>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <div class="mt-4">
                        {% for category, message in messages %}
                            <div class="alert alert-{{ category }}">{{ message }}</div>
                        {% endfor %}
                    </div>
                {% endif %}
            {% endwith %}
        </main>
    </body>
    </html>
    """)

# Admin Login Processing
@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form['admin_username']
    password = request.form['admin_password']
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE Username = %s AND Password = %s AND UserType = 'admin'", (username, password))
    admin = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if admin:
        flash('Admin login successful!', 'success')
        return redirect(url_for('start_page'))
    else:
        flash('Invalid admin credentials!', 'danger')
        return redirect(url_for('admin_login_page'))

# Register Student
@app.route('/register_student', methods=['POST'])
def register_student():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    age = request.form['age']
    phone_number = request.form['phone_number']
    marks10th = request.form['marks10th']
    marks12th = request.form['marks12th']
    department_id = request.form['department_id']
    course = request.form['course']
    profile_image = request.files['profile_image']
    
    profile_image_path = None
    if profile_image:
        filename = secure_filename(profile_image.filename)
        profile_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        profile_image.save(profile_image_path)
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Users (Username, Password, UserType) VALUES (%s, %s, 'student')", (username, password))
        new_user_id = cursor.lastrowid
        
        cursor.execute(""" 
            INSERT INTO Students 
            (FirstName, LastName, Email, Age, PhoneNumber, Marks10th, Marks12th, ProfileImagePath, DepartmentID, Course, UserID) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, email, age, phone_number, marks10th, marks12th, profile_image_path, department_id, course, new_user_id))
        connection.commit()
        flash('Student registered successfully!', 'success')
    except mysql.connector.Error as e:
        connection.rollback()
        flash(f'Error during registration: {e}', 'danger')
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('start_page'))

if __name__ == '__main__':
    app.run(debug=True)
