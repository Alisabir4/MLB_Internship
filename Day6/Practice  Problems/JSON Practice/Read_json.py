import json

with open("students.json","r")as file:
    student=json.load(file)

print(student)