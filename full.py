from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL configurations
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'database': 'college_admission'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        connection.autocommit = True
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# HTML template for student registration page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Engineering College Admission System</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold text-center mb-8">Engineering College Admission System</h1>
        
        <!-- Registration Form -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 class="text-2xl font-semibold mb-4">Student Registration</h2>
            <form id="registrationForm" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">First Name</label>
                        <input type="text" name="first_name" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Last Name</label>
                        <input type="text" name="last_name" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Email</label>
                        <input type="email" name="email" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Phone</label>
                        <input type="tel" name="phone" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Date of Birth</label>
                        <input type="date" name="dob" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Gender</label>
                        <select name="gender" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                            <option value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-gray-700">Address</label>
                        <textarea name="address" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">10th Percentage</label>
                        <input type="number" step="0.01" name="tenth_percentage" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">12th Percentage</label>
                        <input type="number" step="0.01" name="twelfth_percentage" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Entrance Exam Score</label>
                        <input type="number" step="0.01" name="entrance_exam_score" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Preferred Branch</label>
                        <select name="preferred_branch" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                            <option value="">Select Branch</option>
                            <option value="Computer Science">Computer Science</option>
                            <option value="Electronics">Electronics</option>
                            <option value="Mechanical">Mechanical</option>
                            <option value="Civil">Civil</option>
                        </select>
                    </div>
                </div>
                <div class="flex justify-end">
                    <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Submit Application</button>
                </div>
            </form>
        </div>

        <!-- Admin Login Link -->
        <a href="/admin" class="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600 float-right">Admin Login</a>
    </div>

    <script>
        // Handle form submission
        document.getElementById('registrationForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            
            try {
                const response = await fetch('/api/students', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    alert(`Registration successful! Your student ID is: ${result.student_id}`);
                    e.target.reset();
                } else {
                    alert(`Error: ${result.error}`);
                }
            } catch (error) {
                alert('An error occurred during registration');
                console.error('Error:', error);
            }
        });
    </script>
</body>
</html>
'''

# HTML template for the admin login and dashboard page
ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold text-center mb-8">Admin Dashboard</h1>

        <!-- Student List -->
        <table class="min-w-full table-auto bg-white shadow-md rounded-md">
            <thead>
                <tr class="bg-gray-100">
                    <th class="px-4 py-2 text-left">Student ID</th>
                    <th class="px-4 py-2 text-left">Name</th>
                    <th class="px-4 py-2 text-left">Status</th>
                    <th class="px-4 py-2 text-left">Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for student in students %}
                <tr class="border-t">
                    <td class="px-4 py-2">{{ student.student_id }}</td>
                    <td class="px-4 py-2">{{ student.first_name }} {{ student.last_name }}</td>
                    <td class="px-4 py-2">{{ student.status }}</td>
                    <td class="px-4 py-2">
                        <form action="/admin/approve/{{ student.student_id }}" method="POST" class="inline">
                            <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600">Approve</button>
                        </form>
                        <form action="/admin/delete/{{ student.student_id }}" method="POST" class="inline">
                            <button type="submit" class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600">Delete</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
'''

# Root route to display the registration form
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Admin login page (GET and POST)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin_password':
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials, please try again", 403

    # Return the login form for GET requests
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin Login</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
        </head>
        <body class="bg-gray-100">
            <div class="container mx-auto px-4 py-8">
                <h1 class="text-3xl font-bold text-center mb-8">Admin Login</h1>
                <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
                    <form method="POST" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Username</label>
                            <input type="text" name="username" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Password</label>
                            <input type="password" name="password" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                        </div>
                        <button type="submit" class="w-full bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Login</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
    """)

# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT s.student_id, s.first_name, s.last_name, a.status FROM students s JOIN application_status a ON s.student_id = a.student_id")
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template_string(ADMIN_TEMPLATE, students=students)

@app.route('/api/students', methods=['POST'])
def register_student():
    data = request.get_json()
    
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection error"}), 500
    
    try:
        cursor = connection.cursor()
        
        # Insert student data
        cursor.execute("""
            INSERT INTO students (
                first_name, last_name, email, phone, dob, gender, address,
                tenth_percentage, twelfth_percentage, entrance_exam_score, preferred_branch
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get('first_name'), data.get('last_name'), data.get('email'),
            data.get('phone'), data.get('dob'), data.get('gender'), data.get('address'),
            data.get('tenth_percentage'), data.get('twelfth_percentage'),
            data.get('entrance_exam_score'), data.get('preferred_branch')
        ))
        
        student_id = cursor.lastrowid
        
        # Insert initial application status
        cursor.execute("""
            INSERT INTO application_status (student_id, status)
            VALUES (%s, 'Pending')
        """, (student_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"message": "Student registered successfully", "student_id": student_id}), 201
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/approve/<int:student_id>', methods=['POST'])
def approve_student(student_id):
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE application_status
            SET status = 'Approved'
            WHERE student_id = %s
        """, (student_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return redirect(url_for('admin_dashboard'))
    except Error as e:
        return str(e), 500

@app.route('/admin/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500
    
    try:
        cursor = connection.cursor()
        
        # Delete application status first (due to foreign key constraint)
        cursor.execute("DELETE FROM application_status WHERE student_id = %s", (student_id,))
        
        # Then delete student record
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return redirect(url_for('admin_dashboard'))
    except Error as e:
        return str(e), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>404 - Page Not Found</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
        </head>
        <body class="bg-gray-100">
            <div class="container mx-auto px-4 py-8">
                <div class="text-center">
                    <h1 class="text-6xl font-bold text-gray-800 mb-4">404</h1>
                    <p class="text-xl text-gray-600 mb-8">Page not found</p>
                    <a href="/" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Return to Home</a>
                </div>
            </div>
        </body>
        </html>
    """, 404

@app.errorhandler(500)
def server_error(error):
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>500 - Server Error</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
        </head>
        <body class="bg-gray-100">
            <div class="container mx-auto px-4 py-8">
                <div class="text-center">
                    <h1 class="text-6xl font-bold text-gray-800 mb-4">500</h1>
                    <p class="text-xl text-gray-600 mb-8">Internal server error</p>
                    <a href="/" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Return to Home</a>
                </div>
            </div>
        </body>
        </html>
    """, 500

# Database initialization function
def init_db():
    connection = get_db_connection()
    if not connection:
        print("Failed to connect to database")
        return
    
    try:
        cursor = connection.cursor()
        
        # Drop existing tables if they exist
        cursor.execute("DROP TABLE IF EXISTS application_status")
        cursor.execute("DROP TABLE IF EXISTS students")
        
        # Create students table
        cursor.execute("""
            CREATE TABLE students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                dob DATE NOT NULL,
                gender VARCHAR(10) NOT NULL,
                address TEXT NOT NULL,
                tenth_percentage DECIMAL(5,2) NOT NULL,
                twelfth_percentage DECIMAL(5,2) NOT NULL,
                entrance_exam_score DECIMAL(5,2) NOT NULL,
                preferred_branch VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create application_status table
        cursor.execute("""
            CREATE TABLE application_status (
                status_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'Pending',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)
        
        connection.commit()
        print("Database initialized successfully")
        
    except Error as e:
        print(f"Error initializing database: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    # Initialize the database before running the app
    init_db()
    # Run the Flask application
    app.run(debug=True)
