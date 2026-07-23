# Student Performance Dashboard
 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load Dataset
df = pd.read_csv("cleaned_student_performance.csv")


# Total Students

print("Total Students:", len(df))


# Average Score for Each Subject

subject_average = df[[
    "Python",
    "Mathematics",
    "Statistics",
    "Machine_Learning"
]].mean()

print("\nAverage Score for Each Subject:")
print(subject_average)


# Top 5 Performing Students

top_students = df.sort_values(
    by="Average_Score",
    ascending=False
).head(5)

print("\nTop 5 Performing Students:")
print(top_students[["Name", "Average_Score"]])

# Students Needing Improvement

needs_improvement = df[df["Performance"] == "Needs Improvement"]

print("\nStudents Needing Improvement:")
print(needs_improvement[["Name", "Average_Score"]])


# Subject with Highest Average

highest_subject = subject_average.idxmax()
highest_average = subject_average.max()

print("\nSubject with Highest Class Average:")
print(highest_subject, "-", round(highest_average, 2))


#  DATA VISUALIZATION

# Bar Chart - Subject Averages

plt.figure(figsize=(8,5))

plt.bar(subject_average.index, subject_average.values)

plt.title("Average Score of Each Subject")
plt.xlabel("Subjects")
plt.ylabel("Average Marks")

plt.show()

# Bar Chart - Top 5 Students

plt.figure(figsize=(8,5))

plt.bar(top_students["Name"], top_students["Average_Score"])

plt.title("Top 5 Performing Students")
plt.xlabel("Students")
plt.ylabel("Average Score")

plt.show()


# Pie Chart - Performance

performance = df["Performance"].value_counts()

plt.figure(figsize=(6,6))

plt.pie(
    performance,
    labels=performance.index,
    autopct="%1.1f%%"
)

plt.title("Performance Distribution")

plt.show()


# Histogram

plt.figure(figsize=(8,5))

plt.hist(df["Average_Score"], bins=5)

plt.title("Average Score Distribution")
plt.xlabel("Average Score")
plt.ylabel("Frequency")

plt.show()


# Scatter Plot

plt.figure(figsize=(8,5))

plt.scatter(
    df["Python"],
    df["Machine_Learning"]
)

plt.title("Python vs Machine Learning")
plt.xlabel("Python Marks")
plt.ylabel("Machine Learning Marks")

plt.show()


# Box Plot

plt.figure(figsize=(8,5))

sns.boxplot(
    data=df[[
        "Python",
        "Mathematics",
        "Statistics",
        "Machine_Learning"
    ]]
)

plt.title("Marks Distribution Across Subjects")

plt.show()