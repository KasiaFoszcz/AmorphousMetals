"""Hierarchical clustering Streamlit subpage."""

import matplotlib as mpl
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sph
import scipy.spatial.distance as spd
import streamlit as st
from matplotlib import pyplot as plt

from metale_amorficzne import utils
from metale_amorficzne.streamlit.utils import MENU_ITEMS, show_markdown_sibling

st.set_page_config(menu_items=MENU_ITEMS)

st.title("Hierarchical clustering")

results, method = st.tabs(["Results", "Method"])

with method:
    show_markdown_sibling(__file__)


@st.cache_data
def hierarchical_clustering(
    df: pd.DataFrame,
    reference: str,
    features: set[str],
    method: str,
    metric: str,
    normalize_data: bool,
    cluster_count: int,
):
    """Perform hierarchical clustering."""
    # Prepare "clusterable" data.
    hole_map = utils.generate_hole_map(df)
    df_clust = utils.filter_holes(df)
    df_clust = (
        (df_clust - df_clust.mean()) / df_clust.std() if normalize_data else df_clust
    )

    # Prepare figure.
    fig = plt.figure()
    fig.canvas.header_visible = False  # type: ignore
    fig.tight_layout()

    # Show reference image.
    ref_plot = fig.add_subplot(1, 2, 1)
    ref_plot.set_title(f"Reference: {reference}")
    ref_plot.set_axis_off()
    ref_plot.imshow(df[reference].to_numpy().reshape((utils.image_width(df), -1)))

    # Perform clustering.
    clusters = sph.fcluster(
        sph.linkage(df_clust[[*features]], method, metric),
        cluster_count,
        "maxclust",
    )

    # Show clustering result.
    clust_plot = fig.add_subplot(1, 2, 2)
    clust_plot.set_title("Clustered")
    clust_plot.set_axis_off()
    clust_plot.imshow(
        utils.fill_holes(clusters, hole_map).reshape((utils.image_width(df), -1))
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
        df.iloc[[i for i, val in enumerate(clusters) if val == group]].describe()
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
    if "df" not in st.session_state:
        st.columns(3)[1].page_link(
            "pages/02_Data.py", label="Please first upload data here"
        )
    else:
        df: pd.DataFrame = st.session_state.df
        reference = st.selectbox("Select reference feature:", df.columns)
        feature_set = st.selectbox(
            "Select feature set:", ("defaults", "all", "all + XY", "custom")
        )
        match feature_set:
            case "custom":
                features = st.multiselect(
                    "Select features:", df.columns, utils.DEFAULT_COLUMNS
                )
            case "defaults":
                features = list(utils.DEFAULT_COLUMNS)
            case "all + XY":
                features = list(df.columns)
            case other:
                features = list(df.columns)
                features.remove("X [mm]")
                features.remove("Y [mm]")
        st.write("Selected features: *" + "*, *".join(features) + "*.")
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
        normalize_data = st.toggle("Normalize data", True)
        cluster_count = st.slider(
            "Select cluster count:", min_value=2, max_value=10, value=3
        )

        if reference is not None and method is not None and metric is not None:
            hierarchical_clustering(
                df,
                reference,
                set(features),
                method,
                metric,
                normalize_data,
                cluster_count,
            )
