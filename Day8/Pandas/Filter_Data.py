# This Program used where condition are applied

import pandas as pd

student=pd.read_csv("students.csv")

result=student[student["Marks"]>80]
print(result)
