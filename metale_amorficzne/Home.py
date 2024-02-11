import streamlit as st
from pathlib import Path
from metale_amorficzne.streamlit_utils import show_markdown


st.title("Amorphous Metals Analyzer")
show_markdown(__file__, unsafe_allow_html=True)
