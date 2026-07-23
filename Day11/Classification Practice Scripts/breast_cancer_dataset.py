#  This Program shows how to train model using Iris dataset

import pandas as pd

from sklearn.datasets import load_breast_cancer
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

data=load_breast_cancer()

X=data.data
y=data.target

# Explore Dataset

df=pd.DataFrame(X,columns=data.feature_names)
df["Diagnosis"]=y

print("Breat Cancer Dataset")
print("\n First five rows")
print(df.head())

print("\nDataset Shape:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nFeatures_Names")
print(data.feature_names)

print("Target Classes:")
for index,name in enumerate(data.target_names):
    print(f"{index} - > {name}")


print("\n Target Distribution")
print(df["Diagnosis"].value_counts())

# Now Split the datasets

X_train,x_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Then Train model using logistics Regression

model=LogisticRegression(max_iter=200)
model.fit(X_train,y_train)


#  Predicitions

predictions=model.predict(x_test)

# Evaluation


print("\nAccuracy:", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions, average="weighted"))
print("Recall:", recall_score(y_test, predictions, average="weighted"))
print("F1 Score:", f1_score(y_test, predictions, average="weighted"))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report")
print(classification_report(
    y_test,
    predictions,
    target_names=data.target_names
))