nums=[10,34,56,54,78,90]
first=second=(float('-inf'))
for n in nums:
    if n>first:
        second=first
        first=n
    elif first>n>second:
        second=n
print("The second largest number in the list is:",second)    
    