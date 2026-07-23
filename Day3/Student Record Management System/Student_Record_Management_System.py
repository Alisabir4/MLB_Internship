# Student Record management system

students = []


# -------- Add Student --------

def add_student():
    name = input("Enter Name: ")
    roll = input("Enter Roll Number: ")
    age = input("Enter Age: ")
    course = input("Enter Course: ")

    student = {
        "name": name,
        "roll": roll,
        "age": age,
        "course": course
    }

    students.append(student)
    print("Student added successfully!\n")


# -------- View Students --------

def view_students():
    if len(students) == 0:
        print("No students found.\n")
        return

    print("\n--- All Students ---")
    for s in students:
        print(s)

    print("Total Students:", len(students), "\n")


# -------- Search Student --------

def search_student():
    roll = input("Enter Roll Number: ")

    for s in students:
        if s["roll"] == roll:
            print("Student Found:", s, "\n")
            return

    print("Student not found.\n")


# -------- Update Student --------

def update_student():
    roll = input("Enter Roll Number to update: ")

    for s in students:
        if s["roll"] == roll:
            print("Current Data:", s)

            s["name"] = input("Enter new name: ")
            s["age"] = input("Enter new age: ")
            s["course"] = input("Enter new course: ")

            print("Student updated successfully!\n")
            return

    print("Student not found.\n")


# -------- Delete Student --------

def delete_student():
    roll = input("Enter Roll Number to delete: ")

    for s in students:
        if s["roll"] == roll:
            students.remove(s)
            print("Student deleted successfully!\n")
            return

    print("Student not found.\n")


# -------- Menu --------

while True:
    print("===== Student Record System =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        update_student()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid choice!\n")