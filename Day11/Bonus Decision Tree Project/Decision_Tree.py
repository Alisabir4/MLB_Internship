# Iris Flower Classification using Decision Tree

import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Load Dataset


iris = load_iris()

X = iris.data
y = iris.target


# Create DataFrame

df = pd.DataFrame(X, columns=iris.feature_names)
df["Species"] = y


print("IRIS FLOWER CLASSIFICATION USING DECISION TREE")


# Split Dataset

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Decision Tree Model


model = DecisionTreeClassifier(random_state=42)

model.fit(X_train, y_train)


# Make Predictions


predictions = model.predict(X_test)


# Evaluation


print("\nAccuracy :", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions, average="weighted"))
print("Recall   :", recall_score(y_test, predictions, average="weighted"))
print("F1 Score :", f1_score(y_test, predictions, average="weighted"))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report")
print(classification_report(
    y_test,
    predictions,
    target_names=iris.target_names
))


# Sample Predictions


print("\nSample Predictions")

results = pd.DataFrame({
    "Actual": [iris.target_names[i] for i in y_test],
    "Predicted": [iris.target_names[i] for i in predictions]
})

print(results.head(10))