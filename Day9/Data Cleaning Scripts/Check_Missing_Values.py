# This program shows how to check for missing values

import pandas as pd


df=pd.read_csv("student_performance.csv")

print(df.isnull())

