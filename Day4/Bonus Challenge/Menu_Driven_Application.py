# Menu Driven Application 


# Prime number 

def is_prime(num):
    if num < 2:
        return False

    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False

    return True

# Fibonacci series

def fibonacci(n):
    a, b = 0, 1

    print("Fibonacci Series:")
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b
    print()

# Palindrome

def palindrome_check(text):
    if text == text[::-1]:
        print("Palindrome")
    else:
        print("Not Palindrome")

# Multiplication Table

def multiplication_table(num):
    print(f"\nMultiplication Table of {num}")
    for i in range(1, 11):
        print(f"{num} x {i} = {num * i}")

# Menu

while True:
    print("\n===== MENU =====")
    print("1. Check Prime Number")
    print("2. Generate Fibonacci Series")
    print("3. Check Palindrome")
    print("4. Generate Multiplication Table")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        number = int(input("Enter a number: "))

        if is_prime(number):
            print("Prime Number")
        else:
            print("Not a Prime Number")

    elif choice == "2":
        terms = int(input("How many terms? "))
        fibonacci(terms)

    elif choice == "3":
        text = input("Enter a word or number: ")
        palindrome_check(text)

    elif choice == "4":
        number = int(input("Enter a number: "))
        multiplication_table(number)

    elif choice == "5":
        print("Thank you! Program Exited.")
        break

    else:
        print("Invalid choice. Please try again.")