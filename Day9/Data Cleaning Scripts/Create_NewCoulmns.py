# This program show how to create new columns

import pandas as pd

df=pd.read_csv("student_performance.csv")

# Now Create the new column 

df["Average_Score"]=(
    df["Python"]+
    df["Mathematics"]+
    df["Statistics"]+
    df["Machine_Learning"]
)/4
print(df["Average_Score"])

# Basically this program is find row wise average of the entire data

