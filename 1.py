from flask import Flask, render_template_string, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # replace with your database username
    'password': '123456789',  # replace with your database password
    'database': 'admission_systemmm'  # correct database name
}

@app.route('/')
def index():
    return render_template_string(TEMPLATE)

@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form['admin_username']
    password = request.form['admin_password']
    
    # Check admin credentials in the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE Username = %s AND Password = %s AND UserType = 'admin'", (username, password))
    admin = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if admin:
        flash('Admin login successful!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid admin credentials!', 'danger')
        return redirect(url_for('index'))

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
    
    # Register the student in the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        # Insert new user
        cursor.execute("INSERT INTO Users (Username, Password, UserType) VALUES (%s, %s, 'student')", (username, password))
        new_user_id = cursor.lastrowid
        
        # Insert student details
        cursor.execute("INSERT INTO Students (FirstName, LastName, Email, Age, PhoneNumber, Marks10th, Marks12th, UserID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                       (first_name, last_name, email, age, phone_number, marks10th, marks12th, new_user_id))
        connection.commit()
        flash('Student registered successfully!', 'success')
    except mysql.connector.Error as e:
        connection.rollback()
        flash('Error during registration: {}'.format(e), 'danger')
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('index'))

TEMPLATE = '''
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
        <section id="login">
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
        
        <section id="registration" class="mt-4">
            <h2>Student Registration</h2>
            <form action="/register_student" method="POST">
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
                <button type="submit" class="btn btn-success">Register</button>
            </form>
        </section>
    </main>

    <!-- Display Flash Messages -->
    <div class="container mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>
    
    <footer class="text-center mt-4">
        <p>&copy; pradeepta </p>
    </footer>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
