# This program Find the Largest numbers 

num1=int(input("Enter First number: "))
num2=int(input("Enter Second number: "))
num3=int(input("Enter Third number: "))

if num1>num2 and num1>num3:
    print("Largest number is:", num1)
elif num2>num1 and num2>num3:
    print("Largest number is:", num2)
else:
    print("Largest number is:", num3)