## ChatGPT clustering

I read the article and used insights from the author to prepare a prompt for my
data: [*How I Won Singapore’s GPT-4 Prompt Engineering Competition. A deep dive
into the strategies I learned for harnessing the power of Large Language Models
(LLMs)*][LLM] I limited the data input to four chosen parameters for one metal
sample called *Be0_matryca15_50mN_spacing7um_strefa_przejsciowa*. The result was
not entirely wrong, but it was not precise enough to continue trials with this
method.

[LLM]: https://towardsdatascience.com/how-i-won-singapores-gpt-4-prompt-engineering-competition-34c195a93d41#183c

The prompt looked as follows:

```md
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

For each cluster found:
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
- Observation Group: [CLUSTER_NAME]
- Profile: [CLUSTER_INFORMATION]
- HIT Value: [HIT_VALUE]

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
>
> ### Annex
>
> | Cluster Name |   List of Rows|
> |--------------|---------------|
> | Cluster 1    | 0, 1, 15, 16, 17, 18, 23, 31, 32, 33, 34, 44, 45, 46, 47, 51, 52, 53, 54, 61, 62, 63, 64, 65, 70, 71, 76, 77, 78, 81, 84, 85, 90, 91, 92, 93, 94, 95, 96, 97, 98, 105, 106, 107, 108, 111, 116, 119, 124, 125, 126, 127, 128, 131, 133, 134, 135, 136, 137, 138, 139, 144, 145, 146, 147, 151, 152, 153, 155, 156, 158, 159, 160, 161, 162, 163, 166, 167, 169, 170, 172, 173, 174, 175, 178, 179, 182, 184, 188, 189, 190, 193, 195, 197, 201, 203, 206, 210, 211, 214, 215, 217, 218, 220, 221, 223 |
> | Cluster 2    | 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 35, 36, 37, 38, 39, 40, 41, 42, 43, 48, 49, 50, 55, 56, 57, 58, 59, 60, 66, 67, 68, 69, 72, 73, 74, 75, 79, 80, 82, 83, 86, 87, 88, 89, 99, 100, 101, 102, 103, 104, 109, 110, 112, 113, 114, 115, 117, 118, 120, 121, 122, 123, 129, 130, 132, 140, 141, 142, 143, 148, 149, 150, 154, 157, 164, 165, 168, 171, 176, 177, 180, 181, 183, 185, 186, 187, 191, 192, 194, 196, 198, 199, 200, 202, 204, 205, 207, 208, 209, 212, 213, 216, 219, 222 |
> | Cluster 3    | 77, 168, 169, 171, 181, 184, 185, 198, 201, 210, 211, 212, 213, 214, 216, 217, 218, 220, 223, 224 |
>
> This analysis provides a clear segmentation of the dataset into three distinct
> clusters based on mechanical properties, with the average value of HIT
> calculated for each group. If you have any further questions or need
> additional analysis, feel free to ask.
