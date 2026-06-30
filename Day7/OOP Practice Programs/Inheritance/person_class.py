# This program shows person class


class Person():
    def __init__(self,name):
        self.name=name
        
    def introduce(self):
        print(f"My name is {self.name}")
        
p1=Person("Ali")
p2=Person("Honey")

p1.introduce()
p2.introduce()