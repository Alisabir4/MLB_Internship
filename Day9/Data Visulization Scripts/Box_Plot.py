# This program shows how the Box plot visualize the spread of marks in all subjects

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df=pd.read_csv("cleaned_student_performance.csv")

sns.boxplot(
    data=df[["Python","Mathematics","Statistics","Machine_Learning"]]
    
)
plt.title("Marks Distribution")

plt.show()