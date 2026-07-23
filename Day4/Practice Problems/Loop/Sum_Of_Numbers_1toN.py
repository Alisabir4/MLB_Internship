# This program sum of numbers from 1 to N

N=int(input("Enter the value of N: "))
sum=0
for i in range(1,N+1):
    sum=sum+i
print("Sum of numbers from 1 to",N,"is",sum)
    