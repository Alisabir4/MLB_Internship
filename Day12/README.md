# Breast Cancer Prediction System

## Project Overview

This project builds a machine learning classification system to predict whether a breast tumor is **Malignant** or **Benign** using the **Breast Cancer Wisconsin Diagnostic Dataset** available in Scikit-learn.

The project covers data preprocessing, model training, hyperparameter tuning, model evaluation, and confusion matrix visualization.

---

## Dataset

- **Dataset:** Breast Cancer Wisconsin Diagnostic Dataset
- **Source:** Scikit-learn (`load_breast_cancer()`)
- **Classification Type:** Binary Classification

Target Classes:

- **0:** Malignant
- **1:** Benign

---

## Technologies Used

- Python
- Pandas
- Scikit-learn
- Matplotlib

---

## Features

- Load the dataset
- Convert the dataset into a Pandas DataFrame
- Preprocess the data using StandardScaler
- Split the dataset into training and testing sets
- Train a Logistic Regression model
- Perform Hyperparameter Tuning using GridSearchCV
- Evaluate the baseline and tuned models
- Display the best parameters
- Visualize confusion matrices using heatmaps

---

## What I Learned About Model Evaluation

Model evaluation is used to measure how well a machine learning model performs on unseen data. Instead of relying only on training accuracy, multiple evaluation metrics such as Accuracy, Precision, Recall, F1-Score, and the Confusion Matrix provide a better understanding of the model's performance.

---

## What is Hyperparameter Tuning?

Hyperparameter tuning is the process of finding the best model settings before training. In this project, **GridSearchCV** was used to test different combinations of Logistic Regression parameters and automatically select the best-performing configuration using cross-validation.

### Why It Matters

- Improves model performance
- Helps reduce overfitting
- Finds the optimal model configuration
- Produces more reliable predictions

---

## Best Parameters Found by GridSearchCV

The best parameters selected by GridSearchCV are printed when the program runs.

Example:

```python
{'C': 1, 'solver': 'liblinear'}
```

> **Note:** Your output may differ slightly depending on the Scikit-learn version.

---

## Baseline vs Tuned Model

| Model | Accuracy | Precision | Recall | F1-Score |
|--------|----------|-----------|--------|----------|
| Baseline Model | Printed by the program | Printed by the program | Printed by the program | Printed by the program |
| Tuned Model | Printed by the program | Printed by the program | Printed by the program | Printed by the program |

---

## Key Observations

- Logistic Regression performed well on the Breast Cancer dataset.
- GridSearchCV identified the best hyperparameter combination automatically.
- The tuned model achieved performance that was equal to or slightly better than the baseline model.
- Confusion matrix heatmaps made it easier to visualize correct and incorrect predictions.

---
