"""Other methods description Streamlit subpage."""

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import streamlit as st
from sklearn.cluster import OPTICS

import amorphous_metals.streamlit.utils as st_utils
from amorphous_metals import utils
from amorphous_metals.convert import convert_raw_to_df

st.set_page_config(menu_items=st_utils.MENU_ITEMS)

st_utils.show_markdown_sibling(__file__)

gpt, optics = st.tabs(["ChatGPT", "OPTICS"])


def plot_reference(ax) -> pd.DataFrame | None:
    """Plot a reference on Matplotlib axis and return reference data frame."""
    ax.set_axis_off()
    ax.set_aspect(1)
    try:
        ref_df = convert_raw_to_df(
            Path(
                os.getenv(
                    "METAL_DATA_PATH", Path(__file__).parent.parent.parent / "data"
                )
            )
            / "ZrCu alloys/Be0_matryca15_50mN_spacing7um_strefa_przejsciowa.TXT"
        )
        ax.imshow(
            ref_df["HIT (O&P) [MPa]"]
            .to_numpy()
            .reshape((utils.image_width(ref_df), -1))
        )
        return ref_df
    except FileNotFoundError:
        ax.text(
            0.5,
            0.5,
            "Reference data file not found!",
            horizontalalignment="center",
            verticalalignment="center",
            color="red",
        )

    return None


@st_utils.default_st_cache(show_spinner=False)
def plot_gpt_reference():
    """Generate ChatGPT clustering reference plot."""
    fig, ax = plt.subplots(1, 3)
    fig.canvas.header_visible = False  # type: ignore
    fig.tight_layout()

    # Side plots are used for alignment.
    ax[0].set_aspect(1)
    ax[0].set_axis_off()
    ax[2].set_aspect(1)
    ax[2].set_axis_off()

    # Central reference plot.
    plot_reference(ax[1])

    return fig


@st_utils.default_st_cache(show_spinner=False)
def plot_gpt_clustering():
    """Generate ChatGPT clustering result plot."""
    fig = plt.figure(figsize=(14, 7))
    fig.canvas.header_visible = False  # type: ignore
    fig.tight_layout()

    # fmt: off
    groups = [
        [0, 1, 15, 16, 17, 18, 23, 31, 32, 33, 34, 44, 45, 46, 47, 51, 52, 53, 54, 61, 62, 63, 64, 65, 70, 71, 76, 77, 78, 81, 84, 85, 90, 91, 92, 93, 94, 95, 96, 97, 98, 105, 106, 107, 108, 111, 116, 119, 124, 125, 126, 127, 128, 131, 133, 134, 135, 136, 137, 138, 139, 144, 145, 146, 147, 151, 152, 153, 155, 156, 158, 159, 160, 161, 162, 163, 166, 167, 169, 170, 172, 173, 174, 175, 178, 179, 182, 184, 188, 189, 190, 193, 195, 197, 201, 203, 206, 210, 211, 214, 215, 217, 218, 220, 221, 223],
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 35, 36, 37, 38, 39, 40, 41, 42, 43, 48, 49, 50, 55, 56, 57, 58, 59, 60, 66, 67, 68, 69, 72, 73, 74, 75, 79, 80, 82, 83, 86, 87, 88, 89, 99, 100, 101, 102, 103, 104, 109, 110, 112, 113, 114, 115, 117, 118, 120, 121, 122, 123, 129, 130, 132, 140, 141, 142, 143, 148, 149, 150, 154, 157, 164, 165, 168, 171, 176, 177, 180, 181, 183, 185, 186, 187, 191, 192, 194, 196, 198, 199, 200, 202, 204, 205, 207, 208, 209, 212, 213, 216, 219, 222],
        [77, 168, 169, 171, 181, 184, 185, 198, 201, 210, 211, 212, 213, 214, 216, 217, 218, 220, 223, 224]
    ]
    # fmt: on

    for group_i, group in enumerate(groups):
        image = np.zeros(225)

        for pixel in group:
            image[pixel] = 1
        sub = fig.add_subplot(1, len(groups), group_i + 1)
        sub.set_axis_off()
        sub.imshow(image.reshape(15, -1))

    return fig


with gpt:
    st_utils.show_markdown_sibling(__file__, "ChatGPT")

    st.write("Reference image of HIT feature (hardness):")
    st.pyplot(plot_gpt_reference())

    st.write("Given this three clusters, I visualized them with matplotlib:")
    st.pyplot(plot_gpt_clustering())
    st.write(
        """
        Even though one can make out the distinct diagonal line (starting at point 3 and
        ending at point 165) separating Cluster 1 and Cluster 2 in this sample, the rest
        of the clustering performed by ChatGPT is incorrect.
        """
    )


@st_utils.default_st_cache(show_spinner=False)
def plot_optics():
    """Generate OPTICS reference and clustering result plot."""
    fig, ax = plt.subplots(1, 2)
    fig.canvas.header_visible = False  # type: ignore
    fig.tight_layout()

    # Show reference image.
    ax[0].set_title("Reference: HIT (O&P) [MPa]")
    ref_df = plot_reference(ax[0])

    # Run OPTICS clustering with seuclidean distance metric.
    if ref_df is not None:
        clust = OPTICS(
            min_samples=10, xi=0.0001, min_cluster_size=10, metric="precomputed"
        )
        clust.fit(
            scipy.spatial.distance.squareform(
                scipy.spatial.distance.pdist(ref_df, metric="seuclidean")
            )
        )

        ax[1].imshow(clust.labels_.reshape((15, -1)))

    ax[1].set_title("Clustered")
    ax[1].set_axis_off()
    ax[1].set_aspect(1)

    return fig


with optics:
    st_utils.show_markdown_sibling(__file__, "OPTICS")
    st.pyplot(plot_optics())
