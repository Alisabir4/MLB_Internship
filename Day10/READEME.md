# Student Score Prediction System

## Overview

The **Student Score Prediction System** is a Machine Learning project developed using **Python** and **Scikit-learn**. The application loads student performance data, preprocesses it, trains a **Linear Regression** model, predicts students' average scores, evaluates the model, and visualizes the prediction results.

---

## Objectives

* Load the student performance dataset.
* Preprocess the dataset.
* Encode categorical data.
* Create an `Average_Score` column.
* Split the dataset into training and testing sets.
* Apply feature scaling.
* Train a Linear Regression model.
* Predict students' average scores.
* Evaluate the model using MAE, MSE, and R² Score.
* Visualize Actual vs Predicted scores using a scatter plot.

---

## Technologies Used

* Python
* Pandas
* Matplotlib
* Scikit-learn

---

## Project Structure

```text
Student_Score_Prediction_System/
│
├── student_score_prediction.py
├── student_performance.csv
├── Updated_Student_Performance.csv
└── requirements.txt



---

## Machine Learning Workflow

1. Load the dataset.
2. Encode categorical columns.
3. Create the `Average_Score` column.
4. Select feature (`X`) and target (`y`) variables.
5. Split the dataset into training and testing sets.
6. Apply feature scaling using `StandardScaler`.
7. Train a `LinearRegression` model.
8. Predict average scores for the test dataset.
9. Compare Actual and Predicted values.
10. Evaluate the model using:

* Mean Absolute Error (MAE)
* Mean Squared Error (MSE)
* R² Score

11. Visualize the results using a scatter plot.

---

## Evaluation Metrics

The project evaluates the model using:

* **Mean Absolute Error (MAE)** – Average absolute difference between actual and predicted values.
* **Mean Squared Error (MSE)** – Average squared difference between actual and predicted values.
* **R² Score** – Measures how well the model explains the variation in the target variable.

---

## Sample Output

```text
Training Shape: (16, 9)
Testing Shape: (4, 9)

Actual vs Predicted

   Actual  Predicted
0   85.75      85.75
1   97.25      97.25
2   89.50      89.50
3   74.25      74.25

Model Performance

Mean Absolute Error : 0.000000
Mean Squared Error  : 0.000000
R² Score            : 1.00
```

---

## Visualization

The project generates a scatter plot comparing the **Actual Average Scores** and **Predicted Average Scores**. A perfect model produces points that lie close to the diagonal reference line.

---

## Requirements

Install the required libraries before running the project:

```bash
pip install pandas matplotlib scikit-learn
```

Or install them using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## How to Run

1. Place `student_performance.csv` in the project folder.
2. Open the project in VS Code.
3. Activate your Python virtual environment.
4. Run the program:

```bash
python student_score_prediction.py
```

---

## Learning Outcomes

Through this project, I learned:

* Data preprocessing techniques
* Label Encoding
* Feature Scaling
* Train-Test Split
* Building a Linear Regression model
* Making predictions using Scikit-learn
* Evaluating regression models with MAE, MSE, and R² Score
* Visualizing prediction results with Matplotlib

