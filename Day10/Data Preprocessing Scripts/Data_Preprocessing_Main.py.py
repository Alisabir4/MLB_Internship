import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

# Load Dataset
df = pd.read_csv("student_performance.csv")

# Encode categorical columns
encoder = LabelEncoder()

for column in df.select_dtypes(include="object").columns:
    df[column] = encoder.fit_transform(df[column])

# Create Average Score
df["Average_Score"] = df[["Python", "Mathematics", "Statistics","Machine_Learning"]].mean(axis=1)

# Features and Target
X = df.drop("Average_Score", axis=1)
y = df["Average_Score"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Feature Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("Training Shape:", X_train.shape)
print("Testing Shape:", X_test.shape)