# This is an Student Class Program 


class student:
    def __init__(self,name,age,course):
        self.name=name
        self.age=age
        self.course=course
    
    def display(self):
        print(f"Name :{self.name}")  
        print(f"Age :{self.age}")
        print(f"Course:{self.course}")
        
s1=student("Ali",23,"Python")
s2=student("Honey",24,"AI")

s1.display()  
print()
s2.display()    
    