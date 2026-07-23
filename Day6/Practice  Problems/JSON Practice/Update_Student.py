# update the existing table

import json

with open("students.json","r") as file:
    student=json.load(file)
    

student["Course"]="Django"

with open("students.json","w")as file:
    json.dump(student,file,indent=4)
    
print("Updated Sucessfully ")