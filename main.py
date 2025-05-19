import db

def menu():
    db.create_tables()
    while True:
        print("\n1. Insert Student\n2. Insert Result\n3. View Students\n4. View Student Result\n5. View Class Performance")
        print("6. View Student Overall Performance\n7. Delete Student\n8. Modify Student\n9. Exit\n10.Generate Reportcard")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Name: ")
            student_class = input("Class: ")
            age = int(input("Age: "))
            db.insert_student(name, student_class, age)

        elif choice == '2':
            student_id = int(input("Student ID: "))
            subject = input("Subject: ")
            marks = int(input("Marks: "))
            db.insert_result(student_id, subject, marks)

        elif choice == '3':
            for s in db.view_students():
                print(s)

        elif choice == '4':
            student_id = int(input("Student ID: "))
            for r in db.view_student_result(student_id):
                print(r)

        elif choice == '5':
            student_class = input("Class: ")
            for r in db.view_class_performance(student_class):
                print(r)

        elif choice == '6':
            student_id = int(input("Student ID: "))
            avg = db.view_student_overall_performance(student_id)
            print(f"Average Marks: {avg}")

        elif choice == '7':
            student_id = int(input("Student ID: "))
            db.delete_student(student_id)

        elif choice == '8':
            student_id = int(input("Student ID: "))
            current = db.get_student(student_id)

            if current is None:
                print("Student not found.")
                continue

            print(f"Current class: {current[1]}")
            print(f"Current age: {current[2]}")

            new_class = None
            new_age = None

            update_class = input("Do you want to update the class? (y/n): ").strip().lower()
            if update_class == 'y':
                new_class = input("Enter new class: ")

            update_age = input("Do you want to update the age? (y/n): ").strip().lower()
            if update_age == 'y':
                new_age = int(input("Enter new age: "))

            db.update_student(student_id, new_class, new_age)

        elif choice == '9':
            print("Exiting...")
            break
        
        
        elif choice =='10':
            student_id = input("Enter student id to generate report card: ")
            db.generate_report_card(student_id)
        
        else: 
            print("Invalid option")

 

if __name__ == "__main__":
    menu()
