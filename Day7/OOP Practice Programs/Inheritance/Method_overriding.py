#  This program shows how method overrding is applied


class Person:
    
    def introduce(self):
        print("I am a Person")
        
class Student(Person):
    def introduce(self):
        print("I am a Student")
        
s=Student()
s.introduce()