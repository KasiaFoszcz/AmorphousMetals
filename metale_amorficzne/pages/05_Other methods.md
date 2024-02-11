# Other methods

The methods listed in this section were partly or not successful.

## ChatGPT clustering

 I read the article and used insights from the author to prepare a prompt for my
 data: [*How I Won Singapore’s GPT-4 Prompt Engineering Competition. A deep dive
 into the strategies I learned for harnessing the power of Large Language Models
(LLMs)*](https://towardsdatascience.com/how-i-won-singapores-gpt-4-prompt-engineering-competition-34c195a93d41#183c)
I limited the data input to four chosen parameters for one metal sample. The
result was not completely wrong, not precise though to continue trials with this
method.

The prompt looked as follows:

```
 # CONTEXT #
 I analyze mechanical properties of materials. I have a dataset of information
 on my materials: [HVIT, E*, hr, Epsilon, Welast, Wplast].

 #############

 # OBJECTIVE #
 I want you to use the dataset to cluster my the observations into groups and
 then give me the average value of HIT for each group. Use this step-by-step
 process and do not use code:

 1. CLUSTERS: Use the columns of the dataset to cluster the rows of the dataset,
    such that observations within the same cluster have similar column values
    while observations in different clusters have distinctly different column
    values. Ensure that each row only belongs to 1 cluster.

 For each cluster found,
 2. CLUSTER_INFORMATION: Describe the cluster in terms of the dataset columns.
 3. CLUSTER_NAME: Interpret [CLUSTER_INFORMATION] to obtain a short name for the
    observation group in this cluster.
 4. HIT_VALUE: Give me the average value of HIT for each group

 #############

 # STYLE #
 Business analytics report

 #############

 # TONE #
 Professional, technical

 #############

 # AUDIENCE #
 My business partners. Convince them that your clustering is well thought-out
 and fully backed by data.

 #############

 # RESPONSE: MARKDOWN REPORT #
 <For each cluster in [CLUSTERS]>
 — Observation Group: [CLUSTER_NAME]
 — Profile: [CLUSTER_INFORMATION]
 — HIT Value: [HIT_VALUE]

 <Annex> Give a table of the list of all row numbers belonging to each cluster,
 in order to back up your analysis. Use these table headers: [[CLUSTER_NAME],
 List of Rows].

 #############

 # START ANALYSIS #
 If you understand, ask me for my dataset.

```
The following block is the Chat's response.

> Thank you for providing the dataset. Let's proceed with the analysis.
>
> ### Observation Group: Cluster 1
>
> - Profile: This cluster consists of observations with relatively high values
>   for all mechanical properties (HIT, HVIT, EIT, and nit).
> - HIT Value: The average value of HIT for this group is calculated to be
>   approximately 7147.45 MPa.
>
> ### Observation Group: Cluster 2
>
> - Profile: This cluster includes observations with moderate values for all
>   mechanical properties.
> - HIT Value: The average value of HIT for this group is calculated to be
>   approximately 6937.15 MPa.
>
> ### Observation Group: Cluster 3
>
> - Profile: This cluster comprises observations with relatively lower values
>   for all mechanical properties.
> - HIT Value: The average value of HIT for this group is calculated to be
>   approximately 7205.86 MPa.

---

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

- Requires the specification of two parameters: epsilon and the minimum number.
  of points required to form a cluster.
- Can be sensitive to the choice of parameters and the distance metric used.
- May not work well with data that has varying densities or complex shapes.
- Can be computationally expensive for large datasets.

In summary, Density-based clustering is a powerful type of clustering algorithm
that can identify clusters based on the density of data points.
