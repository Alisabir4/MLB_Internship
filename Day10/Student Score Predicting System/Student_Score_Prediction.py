# Student Score Prediction System

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score



# Load Dataset


print("STUDENT SCORE PREDICTION SYSTEM")

df = pd.read_csv("student_performance.csv")

print("\nDataset Loaded Successfully!\n")
print(df.head())

# Encode Categorical Columns


encoder = LabelEncoder()

for column in df.select_dtypes(include="object").columns:
    df[column] = encoder.fit_transform(df[column])

print("\nCategorical Columns Encoded Successfully!")

# Create Average Score

df["Average_Score"] = df[["Python", "Statistics", "Mathematics","Machine_Learning"]].mean(axis=1)

print("\nAverage_Score Column Created!")

# Select Features and Target

X = df.drop("Average_Score", axis=1)
y = df["Average_Score"]

# Split Dataset


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nDataset Split Successfully!")
print("Training Shape:", X_train.shape)
print("Testing Shape :", X_test.shape)

# Feature Scaling


scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("\nFeature Scaling Applied!")

# Create and Train Model

model = LinearRegression()

model.fit(X_train, y_train)

print("\nModel Trained Successfully!")

# Make Predictions


y_pred = model.predict(X_test)


# Actual vs Predicted

comparison = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": y_pred
})

print("\n")

print("Actual vs Predicted")
print(comparison)


# Evaluation Metrics 
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n")
print("Model Performance")


print(f"Mean Absolute Error : {mae:.6f}")
print(f"Mean Squared Error  : {mse:.6f}")
print(f"R² Score            : {r2:.2f}")

# Scatter Plot


plt.figure(figsize=(6, 6))

plt.scatter(y_test, y_pred)

plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    "r--"
)

plt.xlabel("Actual Average Score")
plt.ylabel("Predicted Average Score")
plt.title("Actual vs Predicted Scores")

plt.grid(True)

plt.show()

print("\nPrediction Completed Successfully!")