# Iris Flower Classification System

A Machine Learning classification project that predicts the species of an Iris flower using its physical features. The project uses the **Logistic Regression** algorithm from Scikit-learn to classify flowers into three different species and evaluates the model using multiple performance metrics.

---

## Project Objectives

- Load and explore the Iris dataset.
- Train a Logistic Regression classification model.
- Predict Iris flower species.
- Evaluate the model using different evaluation metrics.
- Display the Confusion Matrix.
- Compare actual and predicted values.
- **Bonus:** Train a Decision Tree model and compare its performance.



## Dataset

This project uses the built-in **Iris Dataset** available in Scikit-learn.

**Dataset Information**

- Total Samples: 150
- Features: 4
- Target Classes: 3

### Features

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

### Target Classes

- Setosa
- Versicolor
- Virginica

---

# What is Classification?

Classification is a supervised machine learning technique used to predict **categories or classes** based on input data.

Examples include:

- Spam or Not Spam
- Disease or Healthy
- Loan Approved or Rejected
- Iris Flower Species

Unlike regression, classification predicts labels instead of numerical values.

---

# Regression vs Classification

| Regression | Classification |
|------------|---------------|
| Predicts numerical values | Predicts categories |
| Output is continuous | Output is discrete |
| Example: House Price Prediction | Example: Iris Species Prediction |
| Linear Regression | Logistic Regression |

---

# Machine Learning Workflow

1. Load Dataset
2. Explore Dataset
3. Split Training and Testing Data
4. Train Logistic Regression Model
5. Make Predictions
6. Evaluate the Model
7. Display Results

---

# Evaluation Metrics Used

The following metrics were used to evaluate the model:

### Accuracy

Measures the percentage of correct predictions.

```
Accuracy = Correct Predictions / Total Predictions
```

---

### Precision

Measures how many predicted positive values were actually correct.

Higher precision means fewer false positives.

---

### Recall

Measures how many actual positive values were correctly identified.

Higher recall means fewer false negatives.

---

### F1-Score

The harmonic mean of Precision and Recall.

It provides a balanced measure of the model's performance.

---

### Confusion Matrix

A table that summarizes prediction results by showing:

- True Positives (TP)
- True Negatives (TN)
- False Positives (FP)
- False Negatives (FN)

---

# Model Performance

Example output:

- Accuracy: **1.00**
- Precision: **1.00**
- Recall: **1.00**
- F1-Score: **1.00**

The model successfully classified all test samples correctly using the selected train-test split.

---

# Observations

- Logistic Regression performed exceptionally well on the Iris dataset.
- The model achieved nearly perfect classification accuracy.
- No significant misclassifications were observed in the Confusion Matrix.
- The Iris dataset is well-structured and suitable for introductory classification tasks.
- The Decision Tree model also achieved high accuracy, making it a good alternative for this dataset.

---

# Technologies Used

- Python
- Pandas
- Scikit-learn
- Logistic Regression

---

# Requirements

Install the required packages:

```bash
pip install pandas scikit-learn
```

---

# How to Run

Run the main project:

```bash
python iris_flower_classification.py
```

Run the bonus project:

```bash
python decision_tree_comparison.py
```

---

# Learning Outcomes

By completing this project, I learned how to:

- Load datasets from Scikit-learn.
- Explore dataset features and target classes.
- Split data into training and testing sets.
- Train a Logistic Regression model.
- Make predictions on unseen data.
- Evaluate model performance using Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
- Compare Logistic Regression with a Decision Tree classifier.


