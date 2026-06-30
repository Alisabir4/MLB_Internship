# This Program shows multiple objects


class Student:
    def __init__(self,name):
        self.name=name
    
    def greet(self):
        print(f"Hello i am {self.name}.")
        
s1=Student("Ali")
s2=Student("Honey")
s3=Student("Ahmad")


s1.greet()
s2.greet()
s3.greet()
    