"""Discussion Streamlit subpage."""

import streamlit as st

import amorphous_metals.streamlit.utils as st_utils

st.set_page_config(menu_items=st_utils.MENU_ITEMS)

st_utils.show_markdown_sibling(__file__)
