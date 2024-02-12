"""Streamlit common utilities."""

from pathlib import Path

import streamlit as st


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
        Path(source_name.replace(".py", ".py" if subpage is None else f"_{subpage}"))
        .with_suffix(".md")
        .read_text("utf8"),
        unsafe_allow_html=unsafe_allow_html,
        **kwargs,
    )
