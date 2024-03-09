"""Streamlit common utilities."""

from dataclasses import dataclass
from functools import cached_property
from importlib.metadata import version
from pathlib import Path
from typing import Any, Callable, Sequence

import matplotlib as mpl
import numpy as np
import numpy.typing as npt
import pandas as pd
import streamlit as st
from streamlit.commands.page_config import MenuItems
from streamlit.delta_generator import DeltaGenerator

from amorphous_metals import utils

MENU_ITEMS: MenuItems = {
    "Report a bug": "https://github.com/KasiaFoszcz/AmorphousMetals/issues",
    "About": f"""
        Data Science postgraduate project at Wroclaw University of Economics and
        Business by Katarzyna Foszcz under supervision of PhD Ryszard Zygała.

        Data from Michał Biały's research of amorphous metals at Wroclaw University of
        Science and Technology.

        Source code available on
        [GitHub](https://github.com/KasiaFoszcz/AmorphousMetals).

        Version: {version("amorphous_metals")}
        """,
}


def default_st_cache(func: Callable[..., Any] | None = None, **kwargs):
    """Cache data Streamlit convenience configuration decorator.

    Can be used either directly on function, or with additional arguments for
    `st.cache_data()`:

    ```
    @default_st_cache
    def cached_func_1():
        ...

    @default_st_cache(show_spinner=False)
    def cached_func_2():
        ...
    ```
    """
    if func is None:
        return st.cache_data(persist="disk", max_entries=100, **kwargs)
    return st.cache_data(persist="disk", max_entries=100, **kwargs)(func)


def get_markdown_sibling(source_name: str, subpage: str | None = None):
    """Get Markdown page accompanying the current Streamlit page file.

    Args:
        source_name -- `__file__` of the caller.
        subpage -- optional subpage name. Defaults to None.
    """
    return (
        Path(source_name.replace(".py", ".py" if subpage is None else f"_{subpage}"))
        .with_suffix(".md")
        .read_text("utf8")
    )


def show_markdown_sibling(
    source_name: str,
    subpage: str | None = None,
    unsafe_allow_html: bool = False,
    **kwargs,
):
    """Show Markdown page accompanying the current Streamlit page file.

    Args:
        source_name -- `__file__` of the caller.
        subpage -- optional subpage name. Defaults to None.
        unsafe_allow_html -- Allow unsafe HTML (passed to `st.markdown()`).
            Defaults to False.
    """
    return st.markdown(
        get_markdown_sibling(source_name, subpage),
        unsafe_allow_html=unsafe_allow_html,
        **kwargs,
    )


def get_image_path(source_name: str, name: str) -> str:
    """Get image path for name relative to page.

    Arguments:
        source_name -- `__file__` of the caller.
        name -- name of the image.

    Returns:
        Absolute path to the image.
    """
    return str(Path(source_name).with_suffix("") / name)


def for_tabs(
    streamlit_func: Callable[[], DeltaGenerator], tabs: Sequence[DeltaGenerator]
) -> tuple[DeltaGenerator, ...]:
    """Use Streamlit function on given set of tabs.

    Arguments:
        streamlit_func -- Streamlit function (e.g., `st.write("Test")`).
        tabs -- sequence of tabs to apply the `streamlit_fun` to.

    Returns:
        Results of `streamlit_func` for all `tabs`.
    """
    results: list[DeltaGenerator] = []
    for tab in tabs:
        with tab:
            results.append(streamlit_func())
    return tuple(results)


@dataclass
class SelectedData:
    """Currently selected data for clustering."""

    df: pd.DataFrame
    reference_name: str
    features: set[str]
    normalize_data: bool


def data_selection() -> SelectedData | None:
    """Show common streamlit components to define clustering input.

    Returns:
        SelectedData or None if no data is defined.
    """
    if "df" not in st.session_state:
        st.columns(3)[1].page_link(
            "pages/02_Data.py", label="Please first upload data here"
        )
        st.stop()

    df: pd.DataFrame = st.session_state.df
    reference_name = st.selectbox("Select reference feature:", df.columns)
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
        case _:
            features = list(df.columns)
            features.remove("X [mm]")
            features.remove("Y [mm]")
    st.write("Selected features: *" + "*, *".join(features) + "*.")
    normalize_data = st.toggle("Normalize data", True)

    if reference_name is None:
        return None

    return SelectedData(df, reference_name, set(features), normalize_data)


def prepare_df_for_clustering(data: SelectedData) -> pd.DataFrame:
    """Prepare data frame for clustering.

    Arguments:
        data -- data input.

    Returns:
        Prepared data frame.
    """
    without_holes = utils.filter_holes(data.df)
    return (
        (without_holes - without_holes.mean()) / without_holes.std()
        if data.normalize_data
        else without_holes
    )


@dataclass(frozen=True)
class ClusteringResult:
    """Result of clustering function."""

    src_df: pd.DataFrame
    """Source data frame for clustering."""
    clusters: npt.NDArray[np.int_]
    """Clustering result, i.e., array of indexes of clusters of rows in src_df."""

    @cached_property
    def filled_clusters(self) -> npt.NDArray[np.int_]:
        """Clusters with all the data holes filled."""
        return utils.fill_holes(self.src_df, self.clusters)


@default_st_cache(show_spinner="Generating clustering summary…")
def clustering_summary(clustering_result: ClusteringResult) -> tuple[pd.DataFrame, ...]:
    """Generate summary for clustering result and show it in Streamlit.

    Arguments:
        clustering_result -- result generated by clustering function.

    Returns:
        Summary data frames for each cluster.
    """
    clust = clustering_result

    # Generate cluster descriptions for points in clusters.
    cluster_desc = tuple(
        clust.src_df.iloc[
            [i for i, val in enumerate(clust.filled_clusters) if val == group]
        ].describe()
        for group in range(min(clust.clusters), max(clust.clusters) + 1)
    )

    # Generate cluster colors used in plot.
    cluster_colors = np.delete(
        mpl.colormaps["viridis"](np.linspace(0, 1, len(cluster_desc))), 3, 1
    )

    # Show results in Streamlit tabs.
    cluster_tabs = st.tabs(
        tuple(f"Cluster {i}" for i in range(1, len(cluster_desc) + 1))
    )
    for tab, desc, color in zip(cluster_tabs, cluster_desc, cluster_colors):
        with tab:
            st.image(color.reshape((1, 1, 3)), width=24)
            st.dataframe(desc)

    return cluster_desc
