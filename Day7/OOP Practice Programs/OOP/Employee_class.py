# This is  an employee class program

class Employee:
    def __init__ (self,name,department,salery):
        self.name=name
        self.department=department
        self.salery=salery
        
    def display(self):
        print(f"Name :{self.name}")
        print(f"Department :{self.department}")
        print(f"Salery :{self.salery}")
        
e1=Employee("Ali","AI / ML",500000)
e2=Employee("Honey","Intern",12000)

e1.display()
print()
e2.display()
    