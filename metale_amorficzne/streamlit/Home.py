"""Streamlit home page."""

import streamlit as st

from metale_amorficzne.streamlit.utils import (
    MENU_ITEMS,
    get_image_path,
    get_markdown_sibling,
)

st.set_page_config(menu_items=MENU_ITEMS)

markdown = get_markdown_sibling(__file__).split("<!-- image_split -->")

st.markdown(markdown[0])
st.image(
    get_image_path(__file__, "process.svg"),
    caption="Clustering process",
    use_column_width="always",
)
st.markdown(markdown[2])
