# KMeans clustering

The most popular partitioning method is the k-means clustering algorithm, which
involves randomly selecting k initial centroids and then iteratively assigning
each data point to the nearest centroid and recalculating the centroid of each
group until the centroids no longer change.

Partitioning Clustering starts by selecting a fixed number of clusters and
randomly assigning data points to each cluster. The algorithm then iteratively
updates the cluster centroids based on the mean or median of the data points in
each cluster.

Next, the algorithm reassigns each data point to the nearest cluster centroid
based on a distance metric. This process is repeated until the algorithm
converges to a stable solution.

## Benefits

- Simple and easy to understand
- Fast and scalable, making it suitable for large datasets.
- Can handle different types of data, including numerical and categorical data.
- Can be used in a wide range of applications.

## Limitations

- Requires the number of clusters to be specified in advance.
- Can be sensitive to the initial placement of cluster centroids.
- May not work well with data that has complex shapes or overlapping clusters.
- Can be affected by outliers or noise in the data.
