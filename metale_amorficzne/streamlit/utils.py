from pathlib import Path

import streamlit as st


def show_markdown_sibling(source_name: str, unsafe_allow_html: bool = False, **kwargs):
    """Show Markdown page acommpanying the current Streamlit page file.

    Args:
        source_name (str): `__file__` of the caller.
        unsafe_allow_html (bool, optional): Allow unsafe HTML (passed to
            `st.markdown()`). Defaults to False.
    """
    return st.markdown(
        Path(source_name).with_suffix(".md").read_text("utf8"),
        unsafe_allow_html=unsafe_allow_html,
        **kwargs
    )
