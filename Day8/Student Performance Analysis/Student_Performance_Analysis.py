# This program shows the analysis of student performance 

import pandas as pd

# Load the Dataset

student=pd.read_csv("student_performance.csv")
print("="*50)
print("student performance dataset")
print("="*50)

# Display the first five and last five

print("\n First Five :")
print(student.head())

print("\n Last Five :")
print(student.tail())

# Display Dataset Information

print("\n Dataset Information :")
print(student.info())

# Find Missing Values

print("\n Missing Values :")
print(student.isnull().sum())

# Calculate the average marks for each subject

print("\n Average Marks :")
print("Python :",student["Python"].mean())
print("Mathematics :",student["Mathematics"].mean())
print("Statistics :",student["Statistics"].mean())
print("Machine_Learning :",student["Machine_Learning"].mean())

# Now Create Total Marks and Average Marks

student["Total_Marks"]=(
    student["Python"]+
    student["Mathematics"]+
    student["Statistics"]+
    student["Machine_Learning"]
)
student["Average_Marks"]=student["Total_Marks"]/4

# Top 5 performing students

print("\n Top 5 Performing Students :")
top_student=student.sort_values(
    by="Average_Marks",
    ascending=False
    
).head(5)

print(top_student[["Student_ID","Name","Average_Marks"]]
)

# Student scoring below the average


    
overall_average = student["Average_Marks"].mean()

print("\nOverall Average Marks:", overall_average)

print("\nStudents Scoring Below Overall Average")

below_average = student[
    student["Average_Marks"] < overall_average
]

print(below_average[
    ["Student_ID", "Name", "Average_Marks"]
])

# Total number of students 

print("\n Total Number of Students :")

print(len(student))

# Save analyze data to new csv

student.to_csv(
    "analyzed_student_performance.csv",
    index=False
    
)
print("\n Analyzed Data Saved Successfully!")

