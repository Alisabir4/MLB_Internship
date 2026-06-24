# This program count number of digits in number

n=int(input("Enter the number: "))
number=n
count=0
while n>0:
    n=n//10
    count=count+1
print("Number of digits in", number, "is", count)
    
    
    
