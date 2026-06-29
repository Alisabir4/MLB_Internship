# Student Record Management System (Updated Version)

## 📌 Project Description

This project is an **updated version** of the Student Record Management System that I built previously.

The original version allowed users to manage student records using Python lists and dictionaries. In this updated version, the project has been enhanced by adding **JSON file handling** and **exception handling**, making the data persistent even after the program is closed.

---

# 🚀 Previous Student Record Management System

The previous version included the following features:

* Add Student
* View All Students
* Search Student by Roll Number
* Update Student Information
* Delete Student Record
* Menu-Driven Program
* Data stored temporarily using Python lists and dictionaries

**Limitation:**
All student records were stored in memory only. When the program was closed, all data was lost.

---

# ✨ Updated Features

The following improvements have been added:

* Save student records to a JSON file
* Automatically load existing student records when the program starts
* Permanently save all changes after adding, updating, or deleting records
* Handle invalid user input using exception handling
* Continue using all CRUD (Create, Read, Update, Delete) operations

Now, student records remain available even after restarting the program.

---

# 🛠️ Technologies Used

* Python 3
* JSON
* File Handling
* Exception Handling

---

# 📁 Project Structure

```text
Updated Student Record Management System/
│
├── student_record_management_system.py
├── students.json

```

---

# ▶️ How to Run

1. Make sure Python 3 is installed.
2. Open the project folder.
3. Create a file named `students.json` with the following content:

```json
[]
```

4. Run the program:

```bash
python student_record_management_system.py
```

---

# 📋 Menu Options

```text
===== Student Record System =====

1. Add Student
2. View Students
3. Search Student
4. Update Student
5. Delete Student
6. Exit
```

---

# 📄 Sample JSON Data

```json
[
    {
        "name": "Ali",
        "roll": "101",
        "age": 22,
        "course": "Python"
    }
]
```

---

# 🎯 Learning Outcomes

This project helped me practice:

* Python Functions
* Lists and Dictionaries
* Conditional Statements
* Loops
* File Handling
* JSON Module
* Exception Handling
* CRUD Operations
* Persistent Data Storage

---

---
