import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        class TEXT NOT NULL,
                        age INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS results (
                        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        subject TEXT,
                        marks INTEGER,
                        FOREIGN KEY(student_id) REFERENCES students(student_id))''')
    conn.commit()

def insert_student(name, student_class, age):
    cursor.execute("INSERT INTO students (name, class, age) VALUES (?, ?, ?)", (name, student_class, age))
    conn.commit()

def insert_result(student_id, subject, marks):
    cursor.execute("INSERT INTO results (student_id, subject, marks) VALUES (?, ?, ?)", (student_id, subject, marks))
    conn.commit()

def view_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()

def view_student_result(student_id):
    cursor.execute("SELECT subject, marks FROM results WHERE student_id = ?", (student_id,))
    return cursor.fetchall()

def view_class_performance(student_class):
    cursor.execute("""SELECT students.name, results.subject, results.marks 
                      FROM students JOIN results ON students.student_id = results.student_id 
                      WHERE students.class = ?""", (student_class,))
    return cursor.fetchall()

def view_student_overall_performance(student_id):
    cursor.execute("SELECT AVG(marks) FROM results WHERE student_id = ?", (student_id,))
    return cursor.fetchone()[0]

def delete_student(student_id):
    cursor.execute("DELETE FROM results WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()

def update_student(student_id, student_class=None, age=None):
    updates = []
    values = []

    if student_class is not None:
        updates.append("class = ?")
        values.append(student_class)

    if age is not None:
        updates.append("age = ?")
        values.append(age)

    if not updates:
        print("No changes provided.")
        return

    values.append(student_id)
    sql = f"UPDATE students SET {', '.join(updates)} WHERE student_id = ?"
    cursor.execute(sql, tuple(values))
    conn.commit()
    print("Student details updated.")


def get_student(student_id):
    cursor.execute("SELECT name, class, age FROM students WHERE student_id = ?", (student_id,))
    return cursor.fetchone()             


def get_grade(marks):
    if marks >= 90:
        return 'A+'
    elif marks >= 80:
        return 'A'
    elif marks >= 70:
        return 'B'
    elif marks >= 60:
        return 'C'
    elif marks >= 50:
        return 'D'
    else:
        return 'F'

def generate_report_card(student_id):
    

    # Fetch student info
    cursor.execute("SELECT name, class FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        print("Student not found.")
        return

    print("\n====== REPORT CARD ======")
    print(f"Name     : {student[0]}")
    print(f"Student id  : {student_id}")
    print(f"Class    : {student[1]}")
    print("--------------------------")
    print("{:<15} {:<10} {:<6}".format("Subject", "Marks", "Grade"))

    # Fetch results
    cursor.execute("SELECT subject, marks FROM results WHERE student_id = ?", (student_id,))
    results = cursor.fetchall()

    if not results:
        print("No results found for this student.")
        return

    total_marks = 0
    for subject, marks in results:
        grade = get_grade(marks)
        print(f"{subject:<15} {marks:<10} {grade:<6}")
        total_marks += marks

    num_subjects = len(results)
    percentage = total_marks / num_subjects
    overall_grade = get_grade(percentage)

    print("--------------------------")
    print(f"Total Marks  : {total_marks}")
    print(f"Percentage   : {percentage:.2f}%")
    print(f"Overall Grade: {overall_grade}")
    print("==========================\n")
    
