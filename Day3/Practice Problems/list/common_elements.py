a=[1,2,3,4,5]
b=[4,5,6,8,9]
common=[]
for i in a:
    if i in b:
        common.append(i)
print("The common elements in the wo lists are :",common)        