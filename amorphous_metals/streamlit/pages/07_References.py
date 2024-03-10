"""References Streamlit subpage."""

import streamlit as st

from amorphous_metals.streamlit import utils

st.set_page_config(menu_items=utils.MENU_ITEMS)

utils.show_markdown_sibling(__file__)
