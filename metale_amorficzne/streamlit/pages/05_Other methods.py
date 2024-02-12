"""Other methods description Streamlit subpage."""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from metale_amorficzne.streamlit.utils import show_markdown_sibling

show_markdown_sibling(__file__)

gpt, optics = st.tabs(["ChatGPT", "OPTICS"])

with gpt:
    show_markdown_sibling(__file__, "ChatGPT")

    st.write("Given this three clusters, I visualized them with matplotlib:")
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
        fig.add_subplot(1, len(groups), group_i + 1).imshow(image.reshape(15, -1))

    st.pyplot(fig)
    st.write(
        """
        Even though one can make out the distinct diagonal line (starting at point 3 and
        ending at point 165) separating Cluster 1 and Cluster 2 in this sample, the rest
        of the clustering performed by ChatGPT is incorrect.
        """
    )

with optics:
    show_markdown_sibling(__file__, "OPTICS")
