"""KMeans clustering Streamlit subpage."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from streamlit_image_coordinates import streamlit_image_coordinates

import amorphous_metals.streamlit.utils as st_utils
from amorphous_metals import utils

st.set_page_config(menu_items=st_utils.MENU_ITEMS)

st.title("K-means clustering")

results, method = st.tabs(["Results", "Method"])

with method:
    st_utils.show_markdown_sibling(__file__)


@st_utils.default_st_cache(show_spinner=False)
def get_row_from_point(df: pd.DataFrame, point: tuple[int, int]):
    """Get row from data frame based on image coordinates.

    Arguments:
        df -- source data frame.
        point -- point coordinates (x, y).

    Returns:
        Selected row from df.
    """
    return df.iloc[point[0] + point[1] * utils.image_width(df)]


@st_utils.default_st_cache(show_spinner="Performing K-means clustering")
def kmeans_clustering(
    data: st_utils.SelectedData, points: list[tuple[int, int]]
) -> st_utils.ClusteringResult:
    """Perform k-means clustering.

    Arguments:
        data -- data input.
        points -- selected initial points.
    """
    df_clust = st_utils.prepare_df_for_clustering(data)
    image_width = utils.image_width(data.df)

    rows = np.array(
        [
            get_row_from_point(data.df[[*data.features]], point).to_numpy()
            for point in points
        ]
    )
    clusters = (
        KMeans(n_clusters=len(rows), init=rows, max_iter=2000).fit(df_clust).labels_
    )

    # Prepare figure.
    fig = plt.figure()
    fig.canvas.header_visible = False  # type: ignore

    clust_plot = fig.add_subplot(1, 1, 1)
    clust_plot.set_axis_off()
    clust_plot.imshow(utils.fill_holes(data.df, clusters).reshape((image_width, -1)))

    # Show plot in Streamlit.
    st.pyplot(fig)

    return st_utils.ClusteringResult(data.df, clusters)


with results:
    selected_data = st_utils.data_selection()
    if selected_data is None:
        st.stop()
    assert selected_data is not None

    reference = utils.filter_holes(
        selected_data.df[[selected_data.reference_name]]
    ).to_numpy()

    # Normalization.
    reference -= np.min(reference)
    reference /= np.max(reference)

    # Map to matplotlib colors.
    REP_COUNT = 22
    reference = (
        utils.fill_holes(
            selected_data.df,
            np.delete(mpl.colormaps["viridis"](reference), 3, 2),
            fill_with=np.array([[1, 1, 1]]),
        ).reshape((utils.image_width(selected_data.df), -1, 3))
        * 255
    ).astype(np.uint8)

    # Color selected points red.
    if "points" not in st.session_state:
        st.session_state.points = []

    for point in st.session_state.points:
        reference[point[1], point[0]] = (255, 0, 0)

    # Upscale the reference image.
    reference = np.repeat(np.repeat(reference, REP_COUNT, 0), REP_COUNT, 1)

    reference_col, clust_result_col = st.columns(2)

    with reference_col:
        # Show the image with coordinate capture.
        value = streamlit_image_coordinates(reference)

        if value is not None:
            point = (value["x"] // REP_COUNT, value["y"] // REP_COUNT)
            if point in st.session_state.points:
                st.session_state.points.remove(point)
                st.rerun()
            elif get_row_from_point(selected_data.df, point).isnull().any():
                st.warning("You cannot choose a point that is a hole.")
            else:
                st.session_state.points.append(point)
                st.rerun()

        # Summary of chosen points.
        summary: list[str] = []
        for index, point in enumerate(st.session_state.points):
            row = get_row_from_point(selected_data.df, point)
            ref_name = selected_data.reference_name
            summary.append(
                f"{index+1}. Value for point x = {point[0]}, y = {point[1]}: "
                f"{row.loc[ref_name]} {ref_name.split()[-1][1:-1]}"
            )
        st.write("\n".join(summary))

        # Reset chosen points.
        if len(st.session_state.points) > 0 and st.button("Reset"):
            st.session_state.points = []
            st.rerun()

    if len(st.session_state.points) == 0:
        clust_result_col.write("Select points for clustering in the image.")
    else:
        with clust_result_col:
            result = kmeans_clustering(selected_data, st.session_state.points)
        st_utils.clustering_summary(result)
