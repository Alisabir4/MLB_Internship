# Iris Flower Clustering & Visualization

## What is Clustering?

Clustering is an unsupervised machine learning technique that groups similar data points into clusters based on their characteristics. Unlike supervised learning, clustering does not require labeled data. In this project, K-Means clustering was used to group Iris flowers into different clusters based on their measurements.

---

## What is PCA?

Principal Component Analysis (PCA) is a dimensionality reduction technique that transforms high-dimensional data into a smaller number of principal components while preserving most of the important information. In this project, PCA reduced the four original features of the Iris dataset to two principal components, making it easier to visualize the data.

---

## How did you determine the best value of K?

The optimal value of **K** was determined using the **Elbow Method**. The Within-Cluster Sum of Squares (WCSS) was calculated for different values of K, and an elbow plot was created. The point where the decrease in WCSS began to level off indicated the optimal number of clusters. For the Iris dataset, the elbow occurred at **K = 3**, which matches the three flower species.

---

## What insights did you gain from the visualizations?

* The Elbow Method indicated that three clusters were the most appropriate for the dataset.
* The K-Means clustering results closely matched the three Iris flower species, although there was slight overlap between Versicolor and Virginica.
* The original data visualization showed how the flowers were distributed based on selected features.
* PCA reduced the dataset from four dimensions to two while preserving most of the variance, making the clusters much easier to visualize and interpret.
* Overall, the visualizations demonstrated that K-Means clustering effectively grouped similar flowers and that PCA is a powerful tool for simplifying high-dimensional data.
