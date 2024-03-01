"""KMeans clustering Streamlit subpage."""

import matplotlib as mpl
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

from amorphous_metals import utils
from amorphous_metals.streamlit.utils import MENU_ITEMS, show_markdown_sibling

st.set_page_config(menu_items=MENU_ITEMS)

st.title("K-means clustering")

results, method = st.tabs(["Results", "Method"])

with method:
    show_markdown_sibling(__file__)

with results:
    # TODO: Move to a function shared with hierarchical clustering.
    if "df" not in st.session_state:
        st.columns(3)[1].page_link(
            "pages/02_Data.py", label="Please first upload data here"
        )
        st.stop()

    df: pd.DataFrame = st.session_state.df
    reference_name = st.selectbox("Select reference feature:", df.columns)
    reference = df[[reference_name]].to_numpy()

    # Normalization.
    reference -= np.min(reference)
    reference /= np.max(reference)

    # Map to matplotlib colors.
    st.write("Select starting points for clustering:")
    REP_COUNT = 20
    reference = (
        np.delete(mpl.colormaps["viridis"](reference), 3, 2).reshape(
            (utils.image_width(df), -1, 3)
        )
        * 256
    ).astype(np.uint8)

    # Color selected points red.
    if "points" not in st.session_state:
        st.session_state.points = []

    for point in st.session_state.points:
        reference[point[1], point[0]] = (255, 0, 0)

    # Upscale the reference image.
    reference = np.repeat(np.repeat(reference, REP_COUNT, 0), REP_COUNT, 1)

    # Show the image with coordinate capture.
    value = streamlit_image_coordinates(reference)
    if value is not None and point not in st.session_state.points:
        st.session_state.points.append(
            (value["x"] // REP_COUNT, value["y"] // REP_COUNT)
        )
        st.rerun()

    # Reset chosen points.
    if len(st.session_state.points) > 0 and st.button("Reset"):
        st.session_state.points = []
        st.rerun()
