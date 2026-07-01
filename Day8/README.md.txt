# Student Performance Analysis using Pandas

## Project Overview

This mini project demonstrates how to use the **Pandas** library to analyze student performance data stored in a CSV file. It is designed for beginners learning Python for Data Science and covers essential Pandas operations such as loading data, exploring datasets, filtering records, calculating statistics, and saving the analyzed data.

---

## Objectives

* Load a CSV dataset using Pandas.
* Display the first and last five rows of the dataset.
* Display dataset information.
* Find missing values.
* Calculate the average marks for each subject.
* Calculate each student's total and average marks.
* Identify the top 5 performing students.
* Find students scoring below the class average.
* Display the total number of students.
* Save the analyzed dataset as a new CSV file.

---

## Project Structure

```text
Student_Performance_Analysis/
│
├── student_performance.csv
├── student_performance_analysis.py
├── analyzed_student_performance.csv

```

---

## Requirements

* Python 3.x
* Pandas

Install Pandas using:

```bash
pip install pandas
```

---

## Dataset

The project uses the following CSV file:

* `student_performance.csv`

The dataset contains student information such as:

* Student ID
* Name
* Age
* Program
* Python Marks
* Mathematics Marks
* Statistics Marks
* Machine Learning Marks
* Attendance

---

## Features

The program performs the following tasks:

1. Loads the student dataset.
2. Displays the first five records.
3. Displays the last five records.
4. Shows dataset information.
5. Checks for missing values.
6. Calculates the average marks for each subject.
7. Creates new columns:

   * Total_Marks
   * Average_Marks
8. Finds the top five performing students.
9. Finds students scoring below the overall average.
10. Displays the total number of students.
11. Saves the analyzed dataset as `analyzed_student_performance.csv`.

---

## How to Run

1. Place `student_performance.csv` in the project folder.
2. Open the terminal in the project directory.
3. Run the following command:

```bash
python student_performance_analysis.py
```

---

## Output

The program displays:

* Dataset preview
* Dataset information
* Missing values
* Subject-wise average marks
* Top 5 students
* Students below average
* Total number of students

A new file named `analyzed_student_performance.csv` is also created containing the calculated columns.

---

## Pandas Concepts Used

* `pd.read_csv()`
* `head()`
* `tail()`
* `info()`
* `isnull()`
* `sum()`
* `mean()`
* `sort_values()`
* Boolean filtering
* Creating new columns
* `len()`
* `to_csv()`

---

## Learning Outcomes

After completing this project, you will be able to:

* Read CSV files using Pandas.
* Explore and inspect datasets.
* Handle missing values.
* Perform data analysis.
* Filter records using conditions.
* Calculate summary statistics.
* Create new columns.
* Save processed data into a new CSV file.


