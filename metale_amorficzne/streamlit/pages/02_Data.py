"""Materials and research methods used for this study Streamlit subpage."""

import math

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from metale_amorficzne import utils
from metale_amorficzne.convert import convert_raw_to_df
from metale_amorficzne.streamlit.utils import show_markdown_sibling

st.title("Data")

input, description = st.tabs(["Data input", "Data description"])

with description:
    show_markdown_sibling(__file__)


@st.cache_data
def show_file(df: pd.DataFrame):
    """Visualize raw file.

    Arguments:
        df -- data frame generated from the file uploaded to Streamlit.

    Returns:
        Data frame representing the input file.
    """
    try:
        st.write(f"Results for file `{df.Name}`:")
    except AttributeError:
        pass

    # Check if there are holes in the data.
    holes = utils.has_holes(df)
    if any(holes):
        st.warning(
            "**Warning:** The data has holes in rows: *"
            + "*, *".join(str(i) for i, hole in enumerate(holes) if hole)
            + "*. Clustering will skip these rows."
        )

    # Show "raw" data frame.
    df_expander = st.expander("Parsed data frame")
    df_expander.dataframe(df)
    df_expander.dataframe(df.describe())

    # Create plots.
    fig = plt.figure(num=df.Name, figsize=(7, 12))
    fig.tight_layout()

    subplot_cols = 4
    subplot_rows = math.ceil(len(df.columns) / subplot_cols)

    for subplot_i, column in enumerate(df):
        a = fig.add_subplot(subplot_rows, subplot_cols, subplot_i + 1)
        a.imshow(df[column].to_numpy().reshape((utils.image_width(df), -1)))
        a.set_title(str(column), fontsize=10)
        a.set_axis_off()

    st.pyplot(fig)


with input:
    input_file = st.file_uploader("Upload the raw data from nanoindenter:", type="txt")
    if input_file is not None:
        try:
            st.session_state.df = convert_raw_to_df(input_file)
        except ValueError as e:
            st.error(f"Parser error: {e}")

    if "df" in st.session_state:
        show_file(st.session_state.df)

        col1, col2 = st.columns(2)
        col1.write(
            '<p align="right">Now, you can perform clustering:</p>',
            unsafe_allow_html=True,
        )
        col2.page_link("pages/03_Hierarchical clustering.py")
