-- Use the created database
USE admission_systemmm;

-- Create Users table for admin and students
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    UserType ENUM('admin', 'student') NOT NULL
);

-- Create Students table
mysql> CREATE TABLE Students (
    ->     StudentID INT AUTO_INCREMENT PRIMARY KEY,
    ->     FirstName VARCHAR(50) NOT NULL,
    ->     LastName VARCHAR(50) NOT NULL,
    ->     Email VARCHAR(100) NOT NULL,
    ->     Age INT,
    ->     PhoneNumber VARCHAR(15),
    ->     Marks10th FLOAT,
    ->     Marks12th FLOAT,
    ->     UserID INT,
    ->     Status ENUM('approved', 'pending', 'denied') DEFAULT 'pending',
    ->     FOREIGN KEY (UserID) REFERENCES Users(UserID)
    -> );

-- Insert a new user
INSERT INTO Users (Username, Password, UserType) VALUES ('student1', 'student_password', 'student');

-- Insert a new student
INSERT INTO Students (FirstName, LastName, Email, Age, PhoneNumber, Marks10th, Marks12th, UserID)
VALUES ('John', 'Doe', 'john.doe@example.com', 18, '1234567890', 85.5, 90.0, LAST_INSERT_ID());

-- Trigger to automatically set rank based on marks
DELIMITER //
CREATE TRIGGER set_student_rank
BEFORE INSERT ON Students
FOR EACH ROW
BEGIN
    IF NEW.Marks12th >= 90 THEN
        SET NEW.Rank = 1;
    ELSEIF NEW.Marks12th >= 80 THEN
        SET NEW.Rank = 2;
    ELSE
        SET NEW.Rank = 3;
    END IF;
END //
DELIMITER ;

-- Procedure to register a new student
DELIMITER //
CREATE PROCEDURE RegisterStudent(
    IN p_Username VARCHAR(50),
    IN p_Password VARCHAR(255),
    IN p_FirstName VARCHAR(50),
    IN p_LastName VARCHAR(50),
    IN p_Email VARCHAR(100),
    IN p_Age INT,
    IN p_PhoneNumber VARCHAR(15),
    IN p_Marks10th FLOAT,
    IN p_Marks12th FLOAT
)
BEGIN
    DECLARE new_user_id INT;

    -- Insert new user
    INSERT INTO Users (Username, Password, UserType) VALUES (p_Username, p_Password, 'student');
    SET new_user_id = LAST_INSERT_ID();

    -- Insert new student details
    INSERT INTO Students (FirstName, LastName, Email, Age, PhoneNumber, Marks10th, Marks12th, UserID)
    VALUES (p_FirstName, p_LastName, p_Email, p_Age, p_PhoneNumber, p_Marks10th, p_Marks12th, new_user_id);
END //
DELIMITER ;

-- Sample Queries
-- Get all students
SELECT * FROM Students;

-- Get a specific student by ID
SELECT * FROM Students WHERE StudentID = 1;

-- Get all students with their approval status
SELECT s.StudentID, s.FirstName, s.LastName, s.Status
FROM Students s
JOIN Users u ON s.UserID = u.UserID
WHERE u.UserType = 'student';

-- Update student status
UPDATE Students
SET Status = 'approved'
WHERE StudentID = 1;

-- Delete a student (cascade to Users table)
DELETE FROM Students WHERE StudentID = 1;

-- Get students who have been approved and have marks greater than the average
SELECT * FROM Students
WHERE Status = 'approved'
AND Marks12th > (SELECT AVG(Marks12th) FROM Students);

-- Get the count of students by approval status
SELECT Status, COUNT(*) AS Count
FROM Students
GROUP BY Status;

-- Get the average marks of approved students
SELECT AVG(Marks12th) AS AverageMarks
FROM Students
WHERE Status = 'approved';

-- Check admin login
SELECT * FROM Users WHERE Username = 'admin_username' AND Password = 'admin_password' AND UserType = 'admin';

-- Check student login
SELECT * FROM Users WHERE Username = 'student_username' AND Password = 'student_password' AND UserType = 'student';



mysql> INSERT INTO Users (Username, Password, UserType) VALUES ('pes1ug23cs819', '9036016116', 'admin');
Query OK, 1 row affected (0.11 sec)
