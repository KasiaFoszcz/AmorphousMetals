"""Streamlit common utilities."""

import math
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
from streamlit.runtime.uploaded_file_manager import UploadedFile

from amorphous_metals import convert

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


@default_st_cache(show_spinner=False)
def convert_raw_to_df(
    raw_input: Path | str | UploadedFile, sort_x_y: bool = False
) -> pd.DataFrame | None:
    """Wrap around convert.convert_raw_to_df with error handling and caching."""
    try:
        return convert.convert_raw_to_df(raw_input, sort_x_y)
    except ValueError as e:
        st.error(f"Parser error: {e}")
    return None


@dataclass
class Point:
    """A point with X and Y coordinates."""

    x: int
    y: int


@dataclass(frozen=True)
class SelectedData:
    """Currently selected data for clustering."""

    df: pd.DataFrame
    reference_name: str
    features: set[str]
    normalize_data: bool

    @cached_property
    def image_width(self) -> int:
        """Get image width for the data frame."""
        return image_width(self.df)

    def get_row_from_point(self, point: Point):
        """Get row from data frame based on image coordinates.

        Arguments:
            point -- point coordinates (x, y).

        Returns:
            Selected row from df.
        """
        return self.df.iloc[point.x + point.y * self.image_width]

    def prepare_df_for_clustering(self) -> pd.DataFrame:
        """Prepare data frame for clustering.

        Returns:
            Prepared data frame.
        """
        without_holes = filter_holes(self.df)[[*self.features]]
        if not self.normalize_data:
            return without_holes
        return ((without_holes - without_holes.mean()) / without_holes.std()).fillna(0)

    def get_reference_image(self):
        """Get square numpy array with selected reference feature image."""
        return self.df[self.reference_name].to_numpy().reshape((self.image_width, -1))

    def get_clustered_image(self, clustered: npt.NDArray[Any]):
        """Get square numpy array with clustering result (with holes filled)."""
        return fill_holes(self.df, clustered).reshape((self.image_width, -1))


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
                "Select features:", df.columns, convert.DEFAULT_COLUMNS
            )
        case "defaults":
            features = list(convert.DEFAULT_COLUMNS)
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
        return fill_holes(self.src_df, self.clusters)

    @default_st_cache(show_spinner="Generating clustering summary…")
    def show_summary(self) -> tuple[pd.DataFrame, ...]:
        """Generate summary for clustering result and show it in Streamlit.

        Arguments:
            clustering_result -- result generated by clustering function.

        Returns:
            Summary data frames for each cluster.
        """
        # Generate cluster descriptions for points in clusters.
        cluster_desc = tuple(
            self.src_df.iloc[
                [i for i, val in enumerate(self.filled_clusters) if val == group]
            ].describe()
            for group in range(min(self.clusters), max(self.clusters) + 1)
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


def image_width(df: pd.DataFrame) -> int:
    """Get (square) image width for the given data frame.

    Arguments:
        df -- source data frame.

    Returns:
        Width/height of the resulting square image.
    """
    return int(math.sqrt(len(df)))


def has_holes(df: pd.DataFrame) -> tuple[bool, ...]:
    """Check if data frame has data holes.

    Arguments:
        df -- source data frame.

    Returns:
        If a row has a hole, the value is True.
    """
    return tuple(df.isnull().any(axis=1))


def filter_holes(df: pd.DataFrame) -> pd.DataFrame:
    """Filter out data holes from data frame.

    Arguments:
        df -- source data frame.

    Returns:
        Data frame without data holes.
    """
    return df[~df.isnull().any(axis=1)]


def generate_hole_map(df: pd.DataFrame) -> tuple[int, ...]:
    """Generate map of clustering to original index.

    If the data frame has some holes (NaN values), they shouldn't be passed to
    clustering algorithms. But once the

    Arguments:
        df -- source data frame.

    Returns:
        Mapping of clustering result index to original data frame index.
    """
    return tuple(row_i for row_i, row in df.iterrows() if not any(row.isnull()))  # type: ignore


def fill_holes(
    source_df: pd.DataFrame, clustered: npt.NDArray[Any], fill_with: Any = math.nan
) -> npt.NDArray[Any]:
    """Fill holes in clustering result.

    Arguments:
        source_df -- source data frame (with holes).
        clustered -- clustering result.

    Keyword Arguments:
        fill_with -- value used to fill the holes with (default: {math.nan}).

    Returns:
        Clustered data with holes filled.
    """
    output = [fill_with for _ in range(len(source_df))]
    for src, dst in enumerate(generate_hole_map(source_df)):
        output[dst] = clustered[src]
    return np.array(output)
