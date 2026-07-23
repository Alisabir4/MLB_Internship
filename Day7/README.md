# Library Management System

## Description

The **Library Management System** is a console-based Python application built using **Object-Oriented Programming (OOP)** concepts. It allows users to manage a collection of books by adding, viewing, searching, borrowing, and returning books. All book records are stored in a **JSON file**, so the data is saved even after the program is closed.

---

## Features

* Add a new book
* View all books
* Search for a book by title
* Borrow a book
* Return a borrowed book
* Store book records in a JSON file
* Handle invalid user input using exception handling
* Data persists between program executions

---

## OOP Concepts Used

* Classes and Objects
* Constructors (`__init__`)
* Attributes and Methods
* Inheritance
* Encapsulation
* Method Reuse

---

## Technologies Used

* Python 3
* JSON
* File Handling
* Exception Handling
* Object-Oriented Programming (OOP)

---

## Project Structure

```
Library_Management_System/
│
├── Library_Management_System.py          # Main application
├── books.json                            # Stores book records


---

## How to Run

1. Make sure Python 3 is installed.
2. Download or clone the project.
3. Open a terminal in the project folder.
4. Run the following command:

```bash
python library.py
```

---

## Menu Options

```
========== Library Management System ==========
1. Add Book
2. View Books
3. Search Book
4. Borrow Book
5. Return Book
6. Exit
```

---

## Sample Book Record (books.json)

```json
[
    {
        "title": "Python Basics",
        "author": "Ali",
        "available": true
    },
    {
        "title": "Django Guide",
        "author": "Ahmed",
        "available": false
    }
]
```

---

## Error Handling

The application handles common errors such as:

* Invalid menu choices
* Non-numeric menu input
* Empty title or author fields
* Searching for a book that does not exist
* Borrowing an already borrowed book
* Returning a book that is already available

---

## Learning Outcomes

By completing this project, you will gain practical experience with:

* Designing applications using OOP
* Working with multiple classes
* Using inheritance
* Reading and writing JSON files
* File handling in Python
* Exception handling
* Building a menu-driven console application

---

## Future Improvements

* Delete a book
* Update book information
* Add book categories
* Add user accounts
* Track borrowing history
* Store borrow and return dates
* Search by author
* Graphical User Interface (GUI)
* Database integration (SQLite or MySQL)


