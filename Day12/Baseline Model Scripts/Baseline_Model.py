# This program shows baseline model

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
    confusion_matrix
    
)

# Load Dataset

cancer=load_breast_cancer()

# Convert to dataframe

df=pd.DataFrame(cancer.data,columns=cancer.feature_names)
df["target"]=cancer.target

# Features and Target

X= df.drop("target",axis=1)
y= df["target"]

# Now split into training and testing

X_train, X_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train logistics regression model
model=LogisticRegression(max_iter=5000)
model.fit(X_train,y_train)

# Predictions

y_predict=model.predict(X_test)

# Evaluate The Model

print("Accuracy :",accuracy_score(y_test,y_predict))
print("Precision :",precision_score(y_test,y_predict))
print("F_1 :",f1_score(y_test,y_predict))
print("Recall :",recall_score(y_test,y_predict))


# Confusion matrix

print("\n Confusion Matrix")
print(confusion_matrix(y_test,y_predict))