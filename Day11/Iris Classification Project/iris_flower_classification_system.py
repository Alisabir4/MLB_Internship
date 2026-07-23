# Iris Flower Classification System

import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
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


# Explore Dataset


df = pd.DataFrame(X, columns=iris.feature_names)
df["Species"] = y

print("=" * 60)
print("IRIS FLOWER CLASSIFICATION SYSTEM")
print("=" * 60)

print("\nFirst Five Rows")
print(df.head())

print("\nDataset Shape:", df.shape)

print("\nFeature Names")
for feature in iris.feature_names:
    print("-", feature)

print("\nTarget Classes")
for index, name in enumerate(iris.target_names):
    print(f"{index} -> {name}")

print("\nTarget Distribution")
print(df["Species"].value_counts())

# Split Dataset


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model

model = LogisticRegression(max_iter=500)

model.fit(X_train, y_train)

# Make Predictions


predictions = model.predict(X_test)

# Evaluation


accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, average="weighted")
recall = recall_score(y_test, predictions, average="weighted")
f1 = f1_score(y_test, predictions, average="weighted")


print("MODEL EVALUATION")


print(f"Accuracy : {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall   : {recall:.2f}")
print(f"F1 Score : {f1:.2f}")

# Confusion Matrix


print("\nConfusion Matrix")

cm = confusion_matrix(y_test, predictions)

print(cm)

# Classification Report

print("\nClassification Report")

print(classification_report(
    y_test,
    predictions,
    target_names=iris.target_names
))

# Sample Predictions



print("SAMPLE PREDICTIONS")


sample_df = pd.DataFrame({
    "Actual": [iris.target_names[i] for i in y_test],
    "Predicted": [iris.target_names[i] for i in predictions]
})

print(sample_df.head(10))