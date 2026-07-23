
# This program shows how to apply these features using OOP concept 


# Add a new book.
# View all books.
# Search for a book.
# Borrow a book.
# Return a book.

import json
import os


# ---------------- This is Book Class ---------------- #

class Book:
    def __init__(self, title, author, available=True):
        self.title = title
        self.author = author
        self.available = available

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "available": self.available
        }


# ---------------- PrintedBook Class (Inheritance) ---------------- #

class PrintedBook(Book):
    def __init__(self, title, author, available=True):
        super().__init__(title, author, available)

    def details(self):
        status = "Available" if self.available else "Borrowed"
        print(f"\nTitle      : {self.title}")
        print(f"Author     : {self.author}")
        print(f"Status     : {status}")


# ---------------- This is  Library Class ---------------- #

class Library:

    FILE_NAME = "books.json"

    def __init__(self):
        self.books = []
        self.load_books()

    # Load Books
    def load_books(self):

        if not os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "w") as file:
                json.dump([], file)

        try:
            with open(self.FILE_NAME, "r") as file:
                data = json.load(file)

            self.books = []

            for book in data:
                self.books.append(
                    PrintedBook(
                        book["title"],
                        book["author"],
                        book["available"]
                    )
                )

        except (json.JSONDecodeError, FileNotFoundError):
            self.books = []

    # Save Books
    def save_books(self):

        data = []

        for book in self.books:
            data.append(book.to_dict())

        with open(self.FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)

    # Add Book
    def add_book(self):

        title = input("Enter Book Title: ").strip()
        author = input("Enter Author Name: ").strip()

        if title == "" or author == "":
            print("Title and Author cannot be empty.")
            return

        self.books.append(PrintedBook(title, author))

        self.save_books()

        print("Book Added Successfully.")

    # View Books
    def view_books(self):

        if len(self.books) == 0:
            print("No Books Available.")
            return

        print("\n===== Library Books =====")

        for book in self.books:
            book.details()

    # Search Book
    def search_book(self):

        title = input("Enter Book Title: ").strip()

        for book in self.books:

            if book.title.lower() == title.lower():
                print("\nBook Found")
                book.details()
                return

        print("Book Not Found.")

    # Borrow Book
    def borrow_book(self):

        title = input("Enter Book Title: ").strip()

        for book in self.books:

            if book.title.lower() == title.lower():

                if book.available:
                    book.available = False
                    self.save_books()
                    print("Book Borrowed Successfully.")
                else:
                    print("Book Already Borrowed.")

                return

        print("Book Not Found.")

    # Return Book
    def return_book(self):

        title = input("Enter Book Title: ").strip()

        for book in self.books:

            if book.title.lower() == title.lower():

                if not book.available:
                    book.available = True
                    self.save_books()
                    print("Book Returned Successfully.")
                else:
                    print("Book is Already Available.")

                return

        print("Book Not Found.")


# ---------------- Main Program ---------------- #

library = Library()

while True:

    print("\n========== Library Management System ==========")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Borrow Book")
    print("5. Return Book")
    print("6. Exit")

    try:

        choice = int(input("Enter your choice: "))

        if choice == 1:
            library.add_book()

        elif choice == 2:
            library.view_books()

        elif choice == 3:
            library.search_book()

        elif choice == 4:
            library.borrow_book()

        elif choice == 5:
            library.return_book()

        elif choice == 6:
            print("Thank you for using the Library Management System.")
            break

        else:
            print("Please enter a number between 1 and 6.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")