"""KMeans clustering Streamlit subpage."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from sklearn.cluster import KMeans
from streamlit_image_coordinates import streamlit_image_coordinates

from amorphous_metals.streamlit import utils

utils.page_head()

st.title("K-means clustering")

results, method = st.tabs(["Results", "Method"])

with method:
    utils.show_markdown_sibling(__file__)


@utils.default_st_cache(show_spinner="Performing K-means clustering")
def kmeans_clustering(
    data: utils.SelectedData, points: list[utils.Point]
) -> utils.ClusteringResult:
    """Perform k-means clustering.

    Arguments:
        data -- data input.
        points -- selected initial points.
    """
    df_clust = data.prepare_df_for_clustering()

    init_rows = np.array(
        [
            data.get_row_from_point(point, data.normalize_data)[[*data.features]]
            for point in points
        ]
    )
    clusters = (
        KMeans(n_clusters=len(init_rows), init=init_rows, max_iter=2000)
        .fit(df_clust)
        .labels_
    )

    # Prepare figure.
    fig, ax = plt.subplots()
    fig.canvas.header_visible = False  # type: ignore
    ax.set_axis_off()
    ax.imshow(data.get_clustered_image(clusters))

    # Show plot in Streamlit.
    st.pyplot(fig)

    return utils.ClusteringResult(data.df, clusters)


REP_COUNT = 22


@st.cache_data(ttl=3600, max_entries=200)
def generate_reference_array(
    selected_data: utils.SelectedData, points: list[utils.Point]
):
    """Generate reference image array for use with streamlit_image_coordinates().

    Arguments:
        selected_data -- data selected for clustering.
        points -- list of selected initial points.

    Returns:
        Reference numpy image array (square with RGB888 pixels).
    """
    # Load reference data without holes.
    reference = utils.filter_holes(
        selected_data.df[[selected_data.reference_name]]
    ).to_numpy()

    # Normalization (0-1) for matplotlib color mapping.
    reference -= np.min(reference)
    reference /= np.max(reference)

    # Map to matplotlib colors (RGB without A).
    reference = np.delete(mpl.colormaps["viridis"](reference), 3, 2)

    # Fill data holes with white color.
    reference = utils.fill_holes(
        selected_data.df, reference, fill_with=np.array([[1, 1, 1]])
    )

    # Make it RGB888 and reshape to square.
    reference = (
        (reference * 255).astype(np.uint8).reshape((selected_data.image_width, -1, 3))
    )

    # Color selected points red.
    for point in points:
        reference[point.y, point.x] = (255, 0, 0)

    # Upscale the reference image.
    return np.repeat(np.repeat(reference, REP_COUNT, 0), REP_COUNT, 1)


with results:
    selected_data = utils.data_selection()
    if selected_data is None:
        utils.page_tail()
    assert selected_data is not None

    if "points" not in st.session_state:
        st.session_state.points = []

    reference_col, clust_result_col = st.columns(2)

    with reference_col:
        # Show the image with coordinate capture.
        value = streamlit_image_coordinates(
            generate_reference_array(selected_data, st.session_state.points)
        )

        if value is not None:
            point = utils.Point(value["x"] // REP_COUNT, value["y"] // REP_COUNT)
            if point in st.session_state.points:
                st.session_state.points.remove(point)
                st.rerun()
            elif selected_data.get_row_from_point(point).isnull().any():
                st.warning("You cannot choose a point that is a hole.")
            else:
                st.session_state.points.append(point)
                st.rerun()

        # Summary of chosen points (value with unit for all coordinates).
        st.write(
            "\n".join(
                f"{index+1}. Value for point x = {point.x}, y = {point.y}: "
                f"{selected_data.get_row_from_point(point).loc[selected_data.reference_name]} "
                f"{selected_data.reference_name.split()[-1][1:-1]}"
                for index, point in enumerate(st.session_state.points)
            )
        )

        # Make it possible to reset chosen points.
        if len(st.session_state.points) > 0 and st.button("Reset"):
            st.session_state.points = []
            st.rerun()

    if len(st.session_state.points) == 0:
        clust_result_col.write("Select points for clustering in the reference image.")
    else:
        with clust_result_col:
            result = kmeans_clustering(selected_data, st.session_state.points)
        result.show_summary()

utils.page_tail()
