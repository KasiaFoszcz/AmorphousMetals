"""References Streamlit subpage."""

from amorphous_metals.streamlit import utils

utils.page_head()
utils.show_markdown_sibling(__file__, unsafe_allow_html=True)
utils.page_tail()
