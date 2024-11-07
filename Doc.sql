-- Use the created database
USE admission_systemmm;

-- Create Users table for admin and students
CREATE TABLE IF NOT EXISTS Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    UserType ENUM('admin', 'student') NOT NULL
);

-- Create Students table
CREATE TABLE IF NOT EXISTS Students (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Age INT,
    PhoneNumber VARCHAR(15),
    Marks10th FLOAT,
    Marks12th FLOAT,
    UserID INT,
    Status ENUM('approved', 'pending', 'denied') DEFAULT 'pending',
    ProfileImagePath VARCHAR(255),
    DepartmentID INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- Create Departments table
CREATE TABLE IF NOT EXISTS Departments (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL UNIQUE
);

-- Create Courses table
CREATE TABLE IF NOT EXISTS Courses (
    CourseID INT AUTO_INCREMENT PRIMARY KEY,
    CourseName VARCHAR(100) NOT NULL UNIQUE,
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- Create StudentCourses table
CREATE TABLE IF NOT EXISTS StudentCourses (
    StudentID INT,
    CourseID INT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID) ON DELETE CASCADE
);

-- Insert Departments data
INSERT INTO Departments (DepartmentName) 
VALUES ('Computer Science'), ('Mechanical Engineering'), ('Electrical Engineering'), ('Civil Engineering');

-- Insert Courses data
INSERT INTO Courses (CourseName, DepartmentID) 
VALUES 
    ('Data Structures', 1), 
    ('Algorithms', 1), 
    ('Computer Networks', 1), 
    ('Thermodynamics', 2), 
    ('Fluid Mechanics', 2);

-- Insert a new admin user
INSERT INTO Users (Username, Password, UserType) 
VALUES ('pes1ug23cs819', '9036016116', 'admin');

-- Insert a new student
INSERT INTO Users (Username, Password, UserType) 
VALUES ('student1', 'student_password', 'student');

-- Insert a new student with the appropriate data
INSERT INTO Students (FirstName, LastName, Email, Age, PhoneNumber, Marks10th, Marks12th, UserID, DepartmentID) 
VALUES ('John', 'Doe', 'john.doe@example.com', 18, '1234567890', 85.5, 90.0, LAST_INSERT_ID(), 1); -- DepartmentID = 1 for Computer Science
