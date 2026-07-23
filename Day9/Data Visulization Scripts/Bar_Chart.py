# This program show how to make bar charts


import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("cleaned_student_performance.csv")

# Create Bar Chart
plt.bar(df["Name"], df["Average_Score"])

plt.title("Average Marks of Each Student")
plt.xlabel("Students")
plt.ylabel("Average Score")

plt.show()

