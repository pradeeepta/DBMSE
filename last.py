from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL configurations
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'database': 'college_admission'}

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
    <title>Student Admission Registration System</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <header class="bg-blue-600 py-4 shadow-md">
        <div class="container mx-auto px-4">
            <h1 class="text-white text-3xl font-bold">College Admission Portal</h1>
        </div>
    </header>

    <div class="container mx-auto px-4 py-8">
        <h2 class="text-2xl font-semibold text-center text-blue-700 mb-6">Register for Admission</h2>
        
        <!-- Registration Form -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8 max-w-3xl mx-auto">
            <h3 class="text-xl font-bold mb-4">Student Registration Form</h3>
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
        <div class="text-center mt-4">
            <a href="/admin" class="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600">Admin Login</a>
        </div>
    </div>

    <footer class="bg-blue-600 py-4 mt-8">
        <div class="container mx-auto text-center text-white">
            &copy; 2024 College Admission Portal..
        </div>
    </footer>

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

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Admission Registration System</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
    </head>
    <body class="bg-gray-100">
        <div class="container mx-auto px-4 py-16">
            <h1 class="text-4xl font-bold text-center text-blue-600 mb-4">Welcome to the Student Admission Registration System</h1>
            <p class="text-xl text-center text-gray-600 mb-12">Streamline your admission process with our easy-to-use platform.</p>

            <div class="flex justify-center space-x-4">
                <a href="/register" class="bg-blue-500 text-white text-lg px-8 py-4 rounded-md hover:bg-blue-600 transition-colors duration-300">
                    Student Registration
                </a>
                <a href="/admin" class="bg-gray-500 text-white text-lg px-8 py-4 rounded-md hover:bg-gray-600 transition-colors duration-300">
                    Admin Login
                </a>
            </div>

            <div class="mt-16 text-center">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">Why Choose Our System?</h2>
                <p class="text-gray-600 leading-relaxed max-w-2xl mx-auto">Our Student Admission Registration System simplifies the admission process for students and administrators alike. Easily register, manage applications, and track admission statuses in one place. Secure and efficient!</p>
            </div>

            <div class="mt-16">
                                <div class="mt-16">
                    
                </div>
            </div>

        </body>
    </html>
    '''

@app.route('/register')
def register():
    return HTML_TEMPLATE

@app.route('/api/students', methods=['POST'])
def register_student():
    try:
        data = request.get_json()
        
        # Connect to MySQL
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor(dictionary=True)
        
        # SQL Query to insert student data
        insert_query = '''
        INSERT INTO students (first_name, last_name, email, phone, dob, gender, address, tenth_percentage, twelfth_percentage, entrance_exam_score, preferred_branch)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        
        values = (
            data['first_name'],
            data['last_name'],
            data['email'],
            data['phone'],
            data['dob'],
            data['gender'],
            data['address'],
            data['tenth_percentage'],
            data['twelfth_percentage'],
            data['entrance_exam_score'],
            data['preferred_branch']
        )
        
        cursor.execute(insert_query, values)
        student_id = cursor.lastrowid  # Get the ID of the newly inserted student

        connection.close()
        
        return jsonify({"student_id": student_id}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Admin login page (no form, just the login UI)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Handle form submission (login check)
        username = request.form.get('username')
        password = request.form.get('password')
        
        # In a real application, you would check these credentials against a database
        if username == "admin" and password == "admin123":
            return redirect('/admin/dashboard')  # Redirect to the admin dashboard upon successful login
        else:
            return 'Invalid credentials, please try again.', 403  # Return an error if login fails
    
    # If GET request, render the login page
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Login - College Admission</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
    </head>
    <body class="bg-gray-100">
        <div class="container mx-auto px-4 py-16">
            <h1 class="text-3xl font-bold text-center text-blue-600 mb-6">Admin Login</h1>
            
            <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-8">
                <form method="POST">
                    <div class="mb-4">
                        <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                        <input type="text" id="username" name="username" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div class="mb-4">
                        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" id="password" name="password" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required>
                    </div>
                    <div class="flex justify-end">
                        <button type="submit" class="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    '''


# Admin Dashboard Route (after login)
# Admin Dashboard Route (after login)
# Admin Dashboard Route (after login)
# Admin Dashboard Route (after login)
# Function to get a connection to the MySQL database


# Admin Dashboard Route
@app.route('/admin/dashboard')
def admin_dashboard():
    try:
        # Connect to MySQL
        connection = get_db_connection()
        if not connection:
            return 'Error connecting to database', 500
        
        cursor = connection.cursor(dictionary=True)

        # Query to fetch student records
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        connection.close()

        # Render the dashboard with student data
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin Dashboard - College Admission</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        </head>
        <body class="bg-gray-100">
            <div class="container mx-auto px-4 py-16">
                <h1 class="text-3xl font-bold text-center text-blue-600 mb-6">Admin Dashboard</h1>
                <p class="text-xl text-center text-gray-600 mb-12">Welcome to the Admin Dashboard</p>

                <div class="max-w-6xl mx-auto bg-white rounded-lg shadow-md p-8">
                    <h2 class="text-2xl font-semibold text-gray-800 mb-6">Student Applications</h2>

                    <div class="overflow-x-auto">
                        <table class="min-w-full table-auto border-collapse border border-gray-300">
                            <thead class="bg-gray-200">
                                <tr>
                                    <th class="px-4 py-2 border">Student ID</th>
                                    <th class="px-4 py-2 border">Name</th>
                                    <th class="px-4 py-2 border">Email</th>
                                    <th class="px-4 py-2 border">Phone</th>
                                    <th class="px-4 py-2 border">Branch</th>
                                    <th class="px-4 py-2 border">10th Marks</th>
                                    <th class="px-4 py-2 border">12th Marks</th>
                                    <th class="px-4 py-2 border">Entrance Exam Score</th>
                                    <th class="px-4 py-2 border">Average Percentage</th>
                                    <th class="px-4 py-2 border">Status</th>
                                    <th class="px-4 py-2 border">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for student in students %}
                                {% set avg_percentage = ((student.tenth_percentage + student.twelfth_percentage + student.entrance_exam_score) / 3) %}
                                <tr class="hover:bg-gray-100">
                                    <td class="px-4 py-2 border">{{ student.student_id }}</td>
                                    <td class="px-4 py-2 border">{{ student.first_name }} {{ student.last_name }}</td>
                                    <td class="px-4 py-2 border">{{ student.email }}</td>
                                    <td class="px-4 py-2 border">{{ student.phone }}</td>
                                    <td class="px-4 py-2 border">{{ student.preferred_branch }}</td>
                                    <td class="px-4 py-2 border">{{ student.tenth_percentage }}%</td>
                                    <td class="px-4 py-2 border">{{ student.twelfth_percentage }}%</td>
                                    <td class="px-4 py-2 border">{{ student.entrance_exam_score }}</td>
                                    <td class="px-4 py-2 border">{{ avg_percentage | round(2) }}%</td>
                                    <td class="px-4 py-2 border">
                                        {% if student.status == 'Approved' %}
                                            <span class="px-2 py-1 bg-green-200 text-green-800 rounded">Approved</span>
                                        {% else %}
                                            <span class="px-2 py-1 bg-yellow-200 text-yellow-800 rounded">Pending</span>
                                        {% endif %}
                                    </td>
                                    <td class="px-4 py-2 border text-center">
                                        {% if student.status != 'Approved' %}
                                            <button onclick="confirmApprove({{ student.student_id }})" class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 mr-2">Approve</button>
                                        {% endif %}
                                        <button onclick="confirmDelete({{ student.student_id }})" class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600">Delete</button>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <script>
                function confirmDelete(studentId) {
                    Swal.fire({
                        title: 'Are you sure?',
                        text: 'Do you want to delete this student record?',
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonColor: '#d33',
                        cancelButtonColor: '#3085d6',
                        confirmButtonText: 'Yes, delete it!'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            fetch(`/admin/delete/${studentId}`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            }).then(response => {
                                if (response.ok) {
                                    Swal.fire(
                                        'Deleted!',
                                        'The student record has been deleted.',
                                        'success'
                                    ).then(() => location.reload());
                                } else {
                                    Swal.fire(
                                        'Error!',
                                        'There was an issue deleting the record.',
                                        'error'
                                    );
                                }
                            });
                        }
                    });
                }

                function confirmApprove(studentId) {
                    Swal.fire({
                        title: 'Approve Application?',
                        text: 'Do you want to approve this student application?',
                        icon: 'question',
                        showCancelButton: true,
                        confirmButtonColor: '#28a745',
                        cancelButtonColor: '#3085d6',
                        confirmButtonText: 'Yes, approve it!'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            fetch(`/admin/approve/${studentId}`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            }).then(response => {
                                if (response.ok) {
                                    Swal.fire(
                                        'Approved!',
                                        'The student application has been approved.',
                                        'success'
                                    ).then(() => location.reload());
                                } else {
                                    Swal.fire(
                                        'Error!',
                                        'There was an issue approving the application.',
                                        'error'
                                    );
                                }
                            });
                        }
                    });
                }
            </script>
        </body>
        </html>
        ''', students=students)

    except Exception as e:
        return f"Error fetching student data: {str(e)}", 500

# Route to approve a student
@app.route('/admin/approve/<int:student_id>', methods=['POST'])
def approve_student(student_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Update the student's status to 'Approved'
        cursor.execute("UPDATE students SET status = 'Approved' WHERE student_id = %s", (student_id,))
        connection.commit()
        connection.close()

        return jsonify({"message": "Student approved successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error approving student: {str(e)}"}), 500

# Route to delete a student
@app.route('/admin/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Delete the student record
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        connection.commit()
        connection.close()

        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error deleting student: {str(e)}"}), 500




if __name__ == '__main__':
    app.run(debug=True)







