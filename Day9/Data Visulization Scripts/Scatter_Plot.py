# This proggram comparing python and machine learning marks

import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("cleaned_student_performance.csv")

plt.scatter(df["Python"],df["Machine_Learning"])

plt.title("Python vs Machine learning")

plt.xlabel("Python Marks")
plt.xlabel("Machine Learning Marks")

plt.show()