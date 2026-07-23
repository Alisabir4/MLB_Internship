students={
    "Ali":99,
    "ahmad":44,
    "sara":88
}

total=0
count=0
for marks in students.values():
    total+=marks
    count+=1
    avearge=total/count
print("avearge marks is :",avearge)