# This tool is analyze numbers

def is_prime(num):
    """Check if a number is Prime or not."""
    if num < 2:
        return False
    for i in range(2,int(num**0.5)+1):
        if num%i==0:
            return False
   
    return True


# This Program will check if the number is Even or Odd

number=int(input("Enter a number : "))
if number%2==0:
    Even_odd="Even"
else:
    Even_odd="Odd"
    
# This Program will check if the number is Prime or not

if is_prime(number):
    prime_status = "a prime number"
else:
    prime_status = "not a prime number"
    
# This program will count the digits in the number

digit_count =len(str(abs(number)))

    
# This program will reverse the number

reverse_number =int(str(abs(number))[::-1])  

# This program will check if the number is Palindrome or not

reverse_number = str(abs(number))[::-1]

if str(abs(number)) == reverse_number:
    palindrome_status = "is a palindrome"
else:
    palindrome_status = "is not a palindrome"
    
# Display the results

print("\n----- The Analysis Report -----")
print(f"Number is : {number}")
print(f"Even/Odd is : {Even_odd}")
print(f"Prime Status is :{prime_status}")
print(f"Digit Count is :{digit_count}")
print(f"Reversed Number is :{reverse_number}")
print(f"Palindrome Status : {palindrome_status}")
    
    