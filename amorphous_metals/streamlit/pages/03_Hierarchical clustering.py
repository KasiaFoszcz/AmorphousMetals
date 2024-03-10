"""Hierarchical clustering Streamlit subpage."""

import scipy.cluster.hierarchy as sph
import scipy.spatial.distance as spd
import streamlit as st
from matplotlib import pyplot as plt

import amorphous_metals.streamlit.utils as utils

st.set_page_config(menu_items=utils.MENU_ITEMS)

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

    methods = list(sph._LINKAGE_METHODS.keys())
    method = st.selectbox(
        "Select clustering method:", methods, methods.index("centroid")
    )
    if method in sph._EUCLIDEAN_METHODS:
        metric = "euclidean"
    else:
        metrics: list[str] = list(spd._METRICS.keys())  # type: ignore
        metric = st.selectbox(
            "Select distance metric:", metrics, metrics.index("euclidean")
        )
    cluster_count = st.slider(
        "Select cluster count:", min_value=2, max_value=10, value=3
    )

    if selected_data is None:
        st.stop()

    if method is not None and metric is not None:
        hierarchical_clustering(
            selected_data, method, metric, cluster_count
        ).show_summary()
