"""Streamlit home page."""

import streamlit as st

from amorphous_metals.streamlit import utils

utils.page_head()

markdown = utils.get_markdown_sibling(__file__).split("<!-- image_split -->")

st.markdown(markdown[0])
st.image(
    utils.get_image_path(__file__, "process.svg"),
    caption="Clustering process",
    use_column_width="always",
)
st.markdown(markdown[2])
# TODO: Remove link to self.
# TODO: Add links to starting point subpages.
# TODO: Add short video on how to use.
# TODO: Use https://github.com/blackary/st_pages with sections.

utils.page_tail()
