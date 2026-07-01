# This program calculate summary and satistics of data

import pandas as pd

student=pd.read_csv("students.csv")
print(student.describe())
