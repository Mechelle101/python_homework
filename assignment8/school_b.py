import sqlite3

# function to enroll a student in a course
def enroll_student(cursor, student, course):
  # first find the student id using their name
  cursor.execute("SELECT student_id FROM Students WHERE name = ?", (student,))
  result = cursor.fetchall()
  
  if len(result) > 0:
    student_id = result[0][0] # first row, first column is the student_id
  else:
    print(f"there was no student named {student}")
    return
  
  # find the course id using the course name
  cursor.execute("SELECT * FROM Courses WHERE course_name = ?", (course,))
  result = cursor.fetchall()
  
  if len(result) > 0:
    course_id = result[0][0] # first row/column (course_id)
  else:
    print(f"There was no course name {course}")
    return
  
  # NOW check if the enrollment exists before inserting
  cursor.execute("SELECT * FROM Enrollments WHERE student_id = ? AND course_id = ?", (student_id, course_id))
  result = cursor.fetchall()
  
  if len(result) > 0:
    print(f"Student {student} is already enrolled in course {course}.")
    return
  
  # insert the enrollment only if it does not already exist
  cursor.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
# ending of the function enroll_student() 
  
# function to add a student
def add_student(cursor, name, age, major):
  try:
    cursor.execute("INSERT INTO Students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
  except sqlite3.IntegrityError:
    print(f"{name} is already in the database.")
# ending of the function add_student()
    
# function to add a course
def add_course(cursor, name, instructor):
  try:
    cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES (?, ?)", (name, instructor))
  except sqlite3.IntegrityError:
    print(f"{name} is already in the database.")
# ending of the function add_course()

# Connect to the database & turn on FK constraints
with sqlite3.connect("../db/school.db") as conn:
    conn.execute("PRAGMA foreign_keys = 1") # Turns on the foreign key constraint
    cursor = conn.cursor()

    # Insert sample data into student table
    add_student(cursor, 'Alice', 20, 'Computer Science')  
    add_student(cursor, 'Bob', 22, 'History')
    add_student(cursor, 'Charlie', 19, 'Biology')
    conn.commit()  # commit the changes to the database
    # Insert sample data into course table
    add_course(cursor, 'Math 101', 'Dr. Smith')
    add_course(cursor, 'English 101', 'Ms. Jones')
    add_course(cursor, 'Chemistry 101', 'Dr. Lee')
    conn.commit() 
    print("Sample data inserted successfully.")
    print()
    # Enroll students in courses
    enroll_student(cursor, "Alice", "Math 101")
    enroll_student(cursor, "Alice", "Chemistry 101")
    enroll_student(cursor, "Bob", "Math 101")
    enroll_student(cursor, "Bob", "English 101")
    enroll_student(cursor, "Charlie", "English 101")
    conn.commit() # more writes, so we have to commit to make them final! (not sure we need multiple commits)
    
    # If you don't commit the transaction, it is rolled back at the end of the with statement, and the data is discarded.
    print("Enrollments added successfully.")
    print()
    
    # Query to verify data insertion
    cursor.execute("SELECT * FROM Students WHERE name='Alice'")
    result = cursor.fetchall()
    for row in result:
      print(row)
    print()
      
    cursor.execute("SELECT * FROM Students")
    print(cursor.fetchall())
    print()
    
    cursor.execute("SELECT student_id, name FROM Students")
    print(cursor.fetchall())
    print()
    
    cursor.execute("SELECT * FROM Courses WHERE instructor_name='Dr. Smith'")
    print(cursor.fetchall())
    print()
    
    cursor.execute("SELECT * FROM Students ORDER BY age")
    print(cursor.fetchall())
    print()
# Ends the with statement and closes the connection
    
    
