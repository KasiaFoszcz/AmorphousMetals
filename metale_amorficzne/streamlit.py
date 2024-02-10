import streamlit as st
from pathlib import Path

cur_dir = Path(__file__).parent

st.title("Amorphous Metals Analyzer")
st.markdown((cur_dir / "description/01_general.md").read_text("utf8"))
