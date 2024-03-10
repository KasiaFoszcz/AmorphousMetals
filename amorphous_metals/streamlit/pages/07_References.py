"""References Streamlit subpage."""

import streamlit as st

import amorphous_metals.streamlit.utils as utils

st.set_page_config(menu_items=utils.MENU_ITEMS)

utils.show_markdown_sibling(__file__)
