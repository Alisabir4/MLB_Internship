# This program shows load and explore dataset

import pandas as pd
from sklearn.datasets import load_iris

# Load

iris=load_iris()

# Create Dataframe

df=pd.DataFrame(iris.data,columns=iris.feature_names)


print("\nFirst five rows ")
print(df.head())

print("\nLast five rows ")
print(df.tail())

print("\nDataset Shapes")
print(df.shape)

print("\n Dataset Information")
print(df.info())

