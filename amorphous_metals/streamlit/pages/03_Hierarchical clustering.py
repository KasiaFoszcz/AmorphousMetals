"""Hierarchical clustering Streamlit subpage."""

import scipy.cluster.hierarchy as sph
import scipy.spatial.distance as spd
import streamlit as st
from matplotlib import pyplot as plt

import amorphous_metals.streamlit.utils as st_utils
from amorphous_metals import utils

st.set_page_config(menu_items=st_utils.MENU_ITEMS)

st.title("Hierarchical clustering")

results, method = st.tabs(["Results", "Method"])

with method:
    st_utils.show_markdown_sibling(__file__)


@st_utils.default_st_cache(show_spinner="Performing hierarchical clustering…")
def hierarchical_clustering(
    data: st_utils.SelectedData, method: str, metric: str, cluster_count: int
) -> st_utils.ClusteringResult:
    """Perform hierarchical clustering."""
    # Prepare "clusterable" data.
    df_clust = st_utils.prepare_df_for_clustering(data)
    image_width = utils.image_width(data.df)

    # Prepare figure.
    fig = plt.figure()
    fig.canvas.header_visible = False  # type: ignore
    fig.tight_layout()

    # Show reference image.
    ref_plot = fig.add_subplot(1, 2, 1)
    ref_plot.set_title(f"Reference: {data.reference_name}")
    ref_plot.set_axis_off()
    ref_plot.imshow(data.df[data.reference_name].to_numpy().reshape((image_width, -1)))

    # Perform clustering.
    clusters = sph.fcluster(
        sph.linkage(df_clust[[*data.features]], method, metric),
        cluster_count,
        "maxclust",
    )

    # Show clustering result.
    clust_plot = fig.add_subplot(1, 2, 2)
    clust_plot.set_title("Clustered")
    clust_plot.set_axis_off()
    clust_plot.imshow(utils.fill_holes(data.df, clusters).reshape((image_width, -1)))

    # Show plot in Streamlit.
    st.pyplot(fig)

    return st_utils.ClusteringResult(data.df, clusters)


with results:
    selected_data = st_utils.data_selection()

    method = st.selectbox(
        "Select clustering method:",
        sph._LINKAGE_METHODS,
        sph._LINKAGE_METHODS["centroid"],
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
        result = hierarchical_clustering(selected_data, method, metric, cluster_count)
        st_utils.clustering_summary(result)
