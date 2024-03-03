"""Hierarchical clustering Streamlit subpage."""

import matplotlib as mpl
import numpy as np
import scipy.cluster.hierarchy as sph
import scipy.spatial.distance as spd
import streamlit as st
from matplotlib import pyplot as plt

from amorphous_metals import utils
from amorphous_metals.streamlit.utils import (
    MENU_ITEMS,
    SelectedData,
    data_selection,
    show_markdown_sibling,
)

st.set_page_config(menu_items=MENU_ITEMS)

st.title("Hierarchical clustering")

results, method = st.tabs(["Results", "Method"])

with method:
    show_markdown_sibling(__file__)


@st.cache_data
def hierarchical_clustering(
    data: SelectedData, method: str, metric: str, cluster_count: int
):
    """Perform hierarchical clustering."""
    # Prepare "clusterable" data.
    hole_map = utils.generate_hole_map(data.df)
    df_clust = utils.filter_holes(data.df)
    df_clust = (
        (df_clust - df_clust.mean()) / df_clust.std()
        if data.normalize_data
        else df_clust
    )

    # Prepare figure.
    fig = plt.figure()
    fig.canvas.header_visible = False  # type: ignore
    fig.tight_layout()

    # Show reference image.
    ref_plot = fig.add_subplot(1, 2, 1)
    ref_plot.set_title(f"Reference: {data.reference_name}")
    ref_plot.set_axis_off()
    ref_plot.imshow(
        data.df[data.reference_name]
        .to_numpy()
        .reshape((utils.image_width(data.df), -1))
    )

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
    clust_plot.imshow(
        utils.fill_holes(clusters, hole_map).reshape((utils.image_width(data.df), -1))
    )

    # Show plot in Streamlit.
    st.pyplot(fig)

    # Show cluster summary.
    ## Generate cluster colors used in plot.
    cluster_colors = np.delete(
        mpl.colormaps["viridis"](np.linspace(0, 1, cluster_count)), 3, 1
    )

    ## Generate cluster descriptions for points in clusters.
    cluster_desc = tuple(
        data.df.iloc[[i for i, val in enumerate(clusters) if val == group]].describe()
        for group in range(1, cluster_count + 1)
    )

    ## Show results in Streamlit tabs.
    cluster_tabs = st.tabs(tuple(f"Cluster {i}" for i in range(1, cluster_count + 1)))
    for tab, desc, color in zip(cluster_tabs, cluster_desc, cluster_colors):
        with tab:
            st.image(color.reshape((1, 1, 3)), width=24)
            st.dataframe(desc)

    return cluster_desc


with results:
    selected_data = data_selection()

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
        hierarchical_clustering(selected_data, method, metric, cluster_count)
