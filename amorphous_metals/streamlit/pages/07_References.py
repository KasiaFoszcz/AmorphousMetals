"""References Streamlit subpage."""

import streamlit as st

from amorphous_metals.streamlit.utils import MENU_ITEMS, show_markdown_sibling

st.set_page_config(menu_items=MENU_ITEMS)

show_markdown_sibling(__file__)
