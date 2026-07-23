import json

with open("students.json","r")as file:
    students=json.load(file)
    
new_student ={
    "name":"honey",
    "age":"21",
    "course":"Django",
    "cgpa":3.55
}
if isinstance(students,list):
    students.append(new_student)
else:
    students=[students,new_student]


with open("students.json","w")as file:
    json.dump(students,file,indent=4)
    
print("New student added")
    