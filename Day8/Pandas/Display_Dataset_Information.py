# This program shows Dataset information

import pandas as pd

student=pd.read_csv("students.csv")

print("Dataset Information :")
print(student.info())

