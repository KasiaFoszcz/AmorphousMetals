"""Materials and research methods used for this study Streamlit subpage."""

import math

import matplotlib.pyplot as plt
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from metale_amorficzne.convert import convert_raw_to_df
from metale_amorficzne.streamlit.utils import show_markdown_sibling
from metale_amorficzne.utils import has_holes

st.title("Data")

input, description = st.tabs(["Data input", "Data description"])

with description:
    show_markdown_sibling(__file__)


def show_file(file: UploadedFile | None):
    """Visualize raw file.

    Arguments:
        file -- file uploaded to Streamlit.

    Returns:
        Data frame representing the input file.
    """
    if input_file is None:
        return

    try:
        df = convert_raw_to_df(input_file)
    except ValueError as e:
        st.error(f"Parser error: {e}")
        return None

    df_expander = st.expander("Parsed data frame")
    df_expander.dataframe(df)
    df_expander.dataframe(df.describe())

    # Check if there are holes in the data.
    holes = has_holes(df)
    if any(holes):
        st.warning(
            "**Warning:** The data has holes in rows: *"
            + ", ".join(str(i) for i, hole in enumerate(holes) if hole)
            + "*. Clustering will skip these rows."
        )

    # Create plots.
    fig = plt.figure(num=df.Name, figsize=(7, 12))
    fig.tight_layout()

    subplot_cols = 4
    subplot_rows = math.ceil(len(df.columns) / subplot_cols)
    image_width = int(math.sqrt(len(df)))

    for subplot_i, column in enumerate(df):
        a = fig.add_subplot(subplot_rows, subplot_cols, subplot_i + 1)
        a.imshow(df[column].to_numpy().reshape((image_width, -1)))
        a.set_title(str(column), fontsize=10)
        a.set_axis_off()

    st.pyplot(fig)

    return df


with input:
    input_file = st.file_uploader("Upload the raw data from nanoindenter:", type="txt")
    df = show_file(input_file)
