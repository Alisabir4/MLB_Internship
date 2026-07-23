# This program shows the flower clustering & visualization

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Load Dataset

iris = load_iris()

df = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

df["Species"] = iris.target


print("First Five Rows")
print(df.head())

print("\n")

print("Dataset Information")
print(df.info())

print("\n")

print("Statistical Summary")
print(df.describe())

print("\n")
print("Missing Values")
print(df.isnull().sum())

# Features

X = df.iloc[:, :-1]

# Elbow Method

wcss = []

for k in range(1, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X)

    wcss.append(model.inertia_)

plt.figure(figsize=(8,5))

plt.plot(range(1,11), wcss, marker="o")

plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS")
plt.grid(True)

plt.show()

# Apply K-Means


kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(X)

df["Cluster"] = clusters

print("\n")


print("Cluster Counts")

print(df["Cluster"].value_counts())


# PCA

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X)

print("\nExplained Variance Ratio")
print(pca.explained_variance_ratio_)

print("\nTotal Explained Variance")
print(pca.explained_variance_ratio_.sum())

# Visualization 1
# Original Data

plt.figure(figsize=(8,6))

plt.scatter(
    X.iloc[:,0],
    X.iloc[:,1],
    c=df["Species"],
    cmap="viridis",
    s=60
)

plt.title("Original Iris Dataset")
plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])

plt.colorbar(label="Species")

plt.show()

# Visualization 2
# K-Means Clusters


plt.figure(figsize=(8,6))

plt.scatter(
    X.iloc[:,0],
    X.iloc[:,1],
    c=clusters,
    cmap="viridis",
    s=60
)

plt.scatter(
    kmeans.cluster_centers_[:,0],
    kmeans.cluster_centers_[:,1],
    marker="X",
    color="red",
    s=220,
    label="Centroids"
)

plt.title("K-Means Clustering")

plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])

plt.legend()

plt.show()

# Visualization 3
# PCA

plt.figure(figsize=(8,6))

plt.scatter(
    X_pca[:,0],
    X_pca[:,1],
    c=clusters,
    cmap="viridis",
    s=60
)

plt.title("PCA Visualization")

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

plt.colorbar(label="Cluster")

plt.show()

# Observations


print("\nPROJECT OBSERVATIONS")

print("1. Three clusters were formed using K-Means.")

print("2. The clusters closely matched the three Iris flower species.")
print("   Some overlap exists between Versicolor and Virginica.")

print("3. PCA reduced four features into two principal components,")
print("   making it much easier to visualize the clusters while")
print("   preserving most of the important information.")