"""Streamlit common utilities."""

from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path
from typing import Callable, Sequence

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
