# Histogram shows the Distribution of Average Scores

import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_csv("cleaned_student_performance.csv")

plt.hist(df["Average_Score"],bins=5)

plt.title("Distribution Of Average Scores")
plt.xlabel("Average Scores")
plt.ylabel("Frequency")
plt.show()