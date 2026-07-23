

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load dataset
cancer = load_breast_cancer()

# Convert dataset to DataFrame
df = pd.DataFrame(cancer.data, columns=cancer.feature_names)
df["target"] = cancer.target

# Features and target
X = df.drop("target", axis=1)
y = df["target"]

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

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

# Best Parameters
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