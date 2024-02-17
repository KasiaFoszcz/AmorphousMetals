Hierarchical clustering (scikit-learn library) gave the best results so far.

Hierarchical clustering is a general family of clustering algorithms that build
nested clusters by merging or splitting them successively. This hierarchy of
clusters is represented as a dendrogram. The root of the tree is the
unique cluster that gathers all the samples, the leaves being the clusters with
only one sample.

The AgglomerativeClustering object performs a hierarchical clustering using a
bottom up approach: each observation starts in its own cluster, and clusters are
successively merged together. The linkage criteria determines the metric used
for the merge strategy:

- Ward minimizes the sum of squared differences within all clusters. It is a
  variance-minimizing approach and in this sense is similar to the- k-means
  objective function but tackled with an agglomerative hierarchical approach.
- Maximum or complete linkage minimizes the maximum distance between
  observations of pairs of clusters.
- Average linkage minimizes the average of the distances between all
  observations of pairs of clusters.
- Single linkage minimizes the distance between the closest observations of
  pairs of clusters.

## Benefits

- Produces a dendrogram that shows the relationships between data points and
  clusters.
- Does not require the number of clusters to be specified in advance.
- Can handle different types of data, including numerical and categorical data.
- Can be used in a wide range of applications.

## Limitations

- Can be computationally expensive and slow for large datasets.
- May not work well with data that has complex shapes or overlapping clusters.
- Can be sensitive to the choice of similarity metric and linkage method.
- Produces a static dendrogram that cannot be easily updated as new data is
  added.
