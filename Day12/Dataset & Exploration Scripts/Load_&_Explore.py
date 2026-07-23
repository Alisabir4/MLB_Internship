import pandas as pd
from sklearn.datasets import load_breast_cancer

# Load dataset
cancer = load_breast_cancer()

# Convert to DataFrame
df = pd.DataFrame(cancer.data, columns=cancer.feature_names)

# Add target column
df["target"] = cancer.target

# Display first 5 rows
print("First 5 Rows:")
print(df.head())

# Display dataset information
print("\nDataset Information:")
print(df.info())

# Display statistical summary
print("\nStatistical Summary:")
print(df.describe())

# Check target class distribution
print("\nTarget Class Distribution:")
print(df["target"].value_counts())
