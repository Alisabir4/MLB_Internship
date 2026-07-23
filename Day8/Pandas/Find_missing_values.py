# This program show how to find mssing values

import pandas as pd

student=pd.read_csv("students.csv")
print(student.isnull())
