# This program shows how  inheritance is applied


class Person:
    def __init__(self,name):
        self.name=name
    
    def showName(self):
        print(f"Name is {self.name}")
        
class Student(Person):
    def study(self):
        print(f"{self.name} is studying")
        
class Teacher(Person):
    def teach(self):
        print(f"{self.name} is teaching")
        
s1=Student("Ahmad")
t1=Teacher("Ali")

# Student

print("------Student------")
s1.showName()
s1.study()

#  Teacher

print("------Teacher--------")
t1.showName()
t1.teach()    