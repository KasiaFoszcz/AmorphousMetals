## OPTICS clustering

The OPTICS clustering method was used to analyze a metal sample called
*Be0_matryca15_50mN_spacing7um_strefa_przejsciowa*. The goal was to handle
clusters of different shapes and identify outliers without needing to specify
the number of clusters in advance. The seuclidean distance metric was used,
which had previously worked well for hierarchical clustering. Additionally, the
minimum size of a cluster was set to 10 points to avoid noisy results. However,
despite these efforts, the method did not provide accurate results as expected.

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
