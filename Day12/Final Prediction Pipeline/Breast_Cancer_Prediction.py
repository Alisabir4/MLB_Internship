# This program predict breast cancer 

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# Load the dataset
cancer = load_breast_cancer()

# Convert to DataFrame
df = pd.DataFrame(cancer.data, columns=cancer.feature_names)
df["target"] = cancer.target

# Features and Target
X = df.drop("target", axis=1)
y = df["target"]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Preprocess the data
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Baseline Model 
baseline_model = LogisticRegression(max_iter=5000)

baseline_model.fit(X_train, y_train)

baseline_predictions = baseline_model.predict(X_test)

print("Baseline Model Performance")
print("Accuracy :", accuracy_score(y_test, baseline_predictions))
print("Precision:", precision_score(y_test, baseline_predictions))
print("Recall   :", recall_score(y_test, baseline_predictions))
print("F1-Score :", f1_score(y_test, baseline_predictions))


# Hyperparameter Tuning

parameters = {
    "C": [0.01, 0.1, 1, 10, 100],
    "solver": ["liblinear", "lbfgs"]
}

grid_search = GridSearchCV(
    estimator=LogisticRegression(max_iter=5000),
    param_grid=parameters,
    cv=5,
    scoring="accuracy"
)

grid_search.fit(X_train, y_train)

print("\nBest Parameters:")
print(grid_search.best_params_)


# Tuned Model

tuned_model = grid_search.best_estimator_

tuned_predictions = tuned_model.predict(X_test)

print("\nTuned Model Performance")
print("Accuracy :", accuracy_score(y_test, tuned_predictions))
print("Precision:", precision_score(y_test, tuned_predictions))
print("Recall   :", recall_score(y_test, tuned_predictions))
print("F1-Score :", f1_score(y_test, tuned_predictions))


# Baseline Confusion Matrix Heatmap

baseline_cm = confusion_matrix(y_test, baseline_predictions)

ConfusionMatrixDisplay(
    confusion_matrix=baseline_cm,
    display_labels=cancer.target_names
).plot(cmap="Blues")

plt.title("Baseline Model Confusion Matrix")
plt.show()


# Tuned Confusion Matrix Heatmap

tuned_cm = confusion_matrix(y_test, tuned_predictions)

ConfusionMatrixDisplay(
    confusion_matrix=tuned_cm,
    display_labels=cancer.target_names
).plot(cmap="Greens")

plt.title("Tuned Model Confusion Matrix")
plt.show()