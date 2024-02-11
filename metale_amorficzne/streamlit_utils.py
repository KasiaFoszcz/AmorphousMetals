import streamlit as st
from pathlib import Path


def show_markdown(source_name: str, unsafe_allow_html: bool = False, **kwargs):
    source_file = Path(source_name)
    st.markdown(
        (source_file.with_suffix(".md")).read_text("utf8"),
        unsafe_allow_html=unsafe_allow_html,
        **kwargs
    )
