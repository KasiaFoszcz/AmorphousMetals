"""Streamlit home page."""

import streamlit as st

from amorphous_metals.streamlit import utils

st.set_page_config(menu_items=utils.MENU_ITEMS)

markdown = utils.get_markdown_sibling(__file__).split("<!-- image_split -->")

st.markdown(markdown[0])
st.image(
    utils.get_image_path(__file__, "process.svg"),
    caption="Clustering process",
    use_column_width="always",
)
st.markdown(markdown[2])
