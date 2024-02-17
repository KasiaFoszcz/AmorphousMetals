"""Streamlit common utilities."""

from pathlib import Path
from typing import Callable, Sequence

import streamlit as st
from streamlit.commands.page_config import MenuItems
from streamlit.delta_generator import DeltaGenerator

MENU_ITEMS: MenuItems = {
    "Report a bug": "https://github.com/KasiaFoszcz/AmorphousMetals/issues",
    "About": """
        Data Science postgraduate project at Wroclaw University of Economics and
        Business by Katarzyna Foszcz under supervision of PhD Ryszard Zygała.

        Data from Michał Biały's research of amorphous metals at Wroclaw University of
        Science and Technology.

        Source code available on
        [GitHub](https://github.com/KasiaFoszcz/AmorphousMetals).
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
