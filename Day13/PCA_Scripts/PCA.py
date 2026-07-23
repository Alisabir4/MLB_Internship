# This Program show PCA using iris Dataset

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

# Load Dataset
iris = load_iris()

df = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

X = df

# Apply PCA

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X)

# Results


print("\nOriginal Shape")
print(X.shape)

print("\n")


print("\nReduced Shape")
print(X_pca.shape)

print("\n")

print("\nExplained Variance Ratio")
print(pca.explained_variance_ratio_)

print("\n")

print("\nTotal Explained Variance")
print(pca.explained_variance_ratio_.sum())


# PCA Visualization

plt.figure(figsize=(8,6))

plt.scatter(
    X_pca[:,0],
    X_pca[:,1],
    c=iris.target,
    cmap="viridis",
    s=70
)

plt.title("PCA Visualization (2 Principal Components)")

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

plt.colorbar(label="Species")

plt.show()