# Pie chart showing the distribution of students by Performance category

import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("cleaned_student_performance.csv")

performance=df["Performance"].value_counts()
plt.pie(
    performance,
    labels=performance.index,
    autopct="%1.1f%%"
)
plt.title("Performance Categories")
plt.show()