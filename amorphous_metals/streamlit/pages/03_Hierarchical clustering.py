"""Hierarchical clustering Streamlit subpage."""

import scipy.cluster.hierarchy as sph
import streamlit as st
from matplotlib import pyplot as plt

from amorphous_metals.streamlit import utils

# Linkage methods and distance metrics documented for
# `scipy.cluster.hierarchy.linkage()` and `scipy.spatial.distance.pdist()`. Defined
# here, as SciPy's own lists are private (`_LINKAGE_METHODS` and `_EUCLIDEAN_METHODS`
# were removed in SciPy 1.18).
LINKAGE_METHODS = [
    "single",
    "complete",
    "average",
    "weighted",
    "centroid",
    "median",
    "ward",
]

# Valid only with Euclidean.
EUCLIDEAN_METHODS = {
    "centroid",
    "median",
    "ward",
}

DISTANCE_METRICS = [
    "braycurtis",
    "canberra",
    "chebyshev",
    "cityblock",
    "correlation",
    "cosine",
    "dice",
    "euclidean",
    "hamming",
    "jaccard",
    "jensenshannon",
    "mahalanobis",
    "minkowski",
    "rogerstanimoto",
    "russellrao",
    "seuclidean",
    "sokalsneath",
    "sqeuclidean",
    "yule",
]

utils.page_head()

st.title("Hierarchical clustering")

results, method = st.tabs(["Results", "Method"])

with method:
    utils.show_markdown_sibling(__file__)


@utils.default_st_cache(show_spinner="Performing hierarchical clustering…")
def hierarchical_clustering(
    data: utils.SelectedData, method: str, metric: str, cluster_count: int
) -> utils.ClusteringResult:
    """Perform hierarchical clustering."""
    # Prepare "clusterable" data.
    df_clust = data.prepare_df_for_clustering()

    # Prepare figure.
    fig = plt.figure()
    fig.canvas.header_visible = False  # type: ignore
    fig.tight_layout()

    # Show reference image.
    ref_plot = fig.add_subplot(1, 2, 1)
    ref_plot.set_title(f"Reference: {data.reference_name}")
    ref_plot.set_axis_off()
    ref_plot.imshow(data.get_reference_image())

    # Perform clustering.
    clusters = sph.fcluster(
        sph.linkage(df_clust, method, metric), cluster_count, "maxclust"
    )

    # Show clustering result.
    clust_plot = fig.add_subplot(1, 2, 2)
    clust_plot.set_title("Clustered")
    clust_plot.set_axis_off()
    clust_plot.imshow(data.get_clustered_image(clusters))

    # Show plot in Streamlit.
    st.pyplot(fig)

    return utils.ClusteringResult(data.df, clusters)


with results:
    selected_data = utils.data_selection()

    method = st.selectbox(
        "Select clustering method:",
        LINKAGE_METHODS,
        LINKAGE_METHODS.index("centroid"),
    )
    if method in EUCLIDEAN_METHODS:
        metric = "euclidean"
    else:
        metric = st.selectbox(
            "Select distance metric:",
            DISTANCE_METRICS,
            DISTANCE_METRICS.index("euclidean"),
        )
    cluster_count = st.slider(
        "Select cluster count:", min_value=2, max_value=10, value=3
    )

    if selected_data is None:
        utils.page_tail()
    assert selected_data is not None

    if method is not None and metric is not None:
        hierarchical_clustering(
            selected_data, method, metric, cluster_count
        ).show_summary()

utils.page_tail()
