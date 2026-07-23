# This program shows the performance of the student

import pandas as pd
df=pd.read_csv("student_performance.csv")

# Create performace columns

def performance(score):
    if score > 90:
        return "Excellent"
    elif score > 80:
        return "Good"
    elif score > 70:
        return "Average"
    else:
        return "Needs Improvements"
    
df["Performance"]=df["Average_Score"].apply(performance)


# Clean Dataset
print("\n Cleaned Dataset :")
print(df.head())

# Save Cleaned Dataset
df.to_csv("cLeaned_student_performance.csv")
print("\n Cleaned Dataset is Saved")
    