
print("Student Grading System")

name=(input("Student Name :"))
student_class=int(input("Class :"))
sub1=(input("Subject 1 name  :"))
sub2=(input("Subject 2 name  :"))
sub3=(input("Subject 3 name  :"))
print("......................")

marks1=int(input(f"Enter {sub1} Marks  :"))
marks2=int(input(f"Enter {sub2}  Marks  :"))
marks3=int(input(f"Enter {sub3}  Marks  :"))
average=(marks1+marks2+marks3)/3
print("......................")
print("student_name",name)
print("student_class",student_class)
print("Average is :" ,average)

if(average<=100 and average>=90):
    print("Excellent")
elif(average<90 and average>=80):
    print("Grade is  A")
elif(average<80 and average>=70):
    print("Grade is  B")
elif(average<70 and average>=60):
    print("Grade is  C")
elif(average<60 and average>=50):
    print("Grade is  D")
else:
    print("Fail")
