"""KMeans clustering Streamlit subpage."""

import streamlit as st

from amorphous_metals.streamlit.utils import MENU_ITEMS, show_markdown_sibling

st.set_page_config(menu_items=MENU_ITEMS)


st.title("KMeans clustering")

results, method = st.tabs(["Results", "Method"])

with method:
    show_markdown_sibling(__file__)

with results:
    st.write("Work in progress…")
