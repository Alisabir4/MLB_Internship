# Student Performance Dashboard

## Project Overview

The **Student Performance Dashboard** is a data analysis project developed using **Python**, **Pandas**, **Matplotlib**, and **Seaborn**. The objective of this project is to clean, analyze, and visualize student performance data to extract meaningful insights and present them in a clear and informative manner.

This project demonstrates fundamental data analysis skills, including data preprocessing, statistical analysis, and data visualization.

---

# Data Cleaning

The dataset was prepared before analysis by performing the following data cleaning operations:

* Inspected the dataset for missing values.
* Removed duplicate records to ensure data consistency.
* Renamed selected columns to improve readability and maintain a consistent naming convention.
* Created a new column named **Average_Score** by calculating the average marks across all academic subjects.
* Generated a **Performance** column based on the following criteria:

  * **Excellent:** Average Score ≥ 90
  * **Good:** Average Score between 80 and 89
  * **Average:** Average Score between 70 and 79
  * **Needs Improvement:** Average Score below 70
* Exported the cleaned dataset as **cleaned_student_performance.csv** for further analysis.

---

# Data Analysis

The following analytical questions were answered:

* Total number of students in the dataset.
* Average score for each subject.
* Top 5 performing students based on their average scores.
* Students who require academic improvement.
* Subject with the highest class average.

---

# Data Visualizations

To make the analysis more intuitive and easier to understand, the following visualizations were created:

### Bar Chart

* Compared the average marks of each subject.
* Displayed the Top 5 performing students.

### Histogram

* Illustrated the distribution of students' average scores.
* Helped understand how student performance is distributed across the class.

### Scatter Plot

* Compared Python and Machine Learning marks.
* Helped identify any relationship between performance in these two subjects.

### Pie Chart

* Showed the percentage distribution of students across different performance categories.

### Box Plot

* Visualized the spread of marks for all subjects.
* Helped identify variability and potential outliers.

---

# Key Insights

* The analysis identified the subject with the highest overall class average.
* The dashboard highlighted the Top 5 highest-performing students based on their Average Score.
* Students classified as **Needs Improvement** were identified, enabling targeted academic support.
* Performance visualizations provided a clear understanding of score distribution and trends across subjects.

---

# Technologies Used

* Python
* Pandas
* Matplotlib
* Seaborn
* CSV Dataset

---

# Project Structure

```text
Student_Performance_Dashboard/
│
├── student_performance.csv
├── cleaned_student_performance.csv
├── Student_Performance_Dashboard.py


# Conclusion

This project demonstrates the complete workflow of a basic data analysis task—from cleaning raw data to generating meaningful insights through visualizations. It showcases essential skills in data preprocessing, exploratory data analysis (EDA), and visualization, providing a strong foundation for more advanced data science and machine learning projects.
