# This program generates the Fibonacci sequence up to a certain number of terms

num_terms=int(input("Enter the number of terms: "))

# First two terms of the Fibonacci sequence
a, b = 0, 1

print("Fibonacci sequence:")
for _ in range(num_terms):
    print(a, end=" ")
    a, b = b, a + b