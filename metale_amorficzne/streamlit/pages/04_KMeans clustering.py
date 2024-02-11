"""KMeans clustering Streamlit subpage."""

import streamlit as st

from metale_amorficzne.streamlit.utils import show_markdown_sibling

st.title("KMeans clustering")

results, method = st.tabs(["Results", "Method"])

with method:
    show_markdown_sibling(__file__)
