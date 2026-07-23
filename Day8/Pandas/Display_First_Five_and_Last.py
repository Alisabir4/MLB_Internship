# this program shows the first and last five rows

import pandas as pd

student=pd.read_csv("students.csv")

print("First Five :")
print(student.head()) # By default head display first five 

print("Last five :")

print(student.tail()) # By default tail display last five