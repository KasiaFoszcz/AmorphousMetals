## OPTICS clustering

This method did not provide good results.

OPTICS, together with DBSCAN are two common algorithms used in Density-based
clustering.

Density-based clustering is a type of clustering algorithm that identifies
clusters as areas of high density separated by areas of low density. The goal is
to group together data points that are close to each other and have a higher
density than the surrounding data points.

### How Does Density-based clustering Work?

Density-based clustering starts by selecting a random data point and identifying
all data points that are within a specified distance (epsilon) from the point.

These data points are considered the core points of a cluster. Next, the
algorithm identifies all data points within the epsilon distance from the core
points and adds them to the cluster. This process is repeated until all data
points have been assigned to a cluster.

### Benefits

- Can identify clusters of varying shapes and sizes.
- Can handle noise and outliers in the data.
- Does not require the number of clusters to be specified in advance.
- Can be used in a wide range of applications.

### Limitations

- Requires the specification of two parameters: epsilon and the minimum number
  of points required to form a cluster.
- Can be sensitive to the choice of parameters and the distance metric used.
- May not work well with data that has varying densities or complex shapes.
- Can be computationally expensive for large datasets.

In summary, Density-based clustering is a powerful type of clustering algorithm
that can identify clusters based on the density of data points.
