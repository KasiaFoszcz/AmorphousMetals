"""Streamlit home page."""

import streamlit as st

import amorphous_metals.streamlit.utils as st_utils

st.set_page_config(menu_items=st_utils.MENU_ITEMS)

markdown = st_utils.get_markdown_sibling(__file__).split("<!-- image_split -->")

st.markdown(markdown[0])
st.image(
    st_utils.get_image_path(__file__, "process.svg"),
    caption="Clustering process",
    use_column_width="always",
)
st.markdown(markdown[2])
