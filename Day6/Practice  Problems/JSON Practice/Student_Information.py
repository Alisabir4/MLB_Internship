import json

student = {
    "name": "Ali",
    "age": 22,
    "course": "Python",
    "cgpa": 3.46
}

with open("students.json", "w") as file:
    json.dump(student, file, indent=4)

print("Student saved.")