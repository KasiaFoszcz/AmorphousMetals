"""Miscellaneous data frame analysis utilities."""

import math
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd

HoleMap = tuple[tuple[int, int], ...]


def has_holes(df: pd.DataFrame) -> tuple[bool, ...]:
    """Check if data frame has data holes.

    Arguments:
        df -- source data frame.

    Returns:
        If a row has a hole, the value is True.
    """
    return tuple(any(row.isna()) for _, row in df.iterrows())


def generate_hole_map(df: pd.DataFrame) -> HoleMap:
    """Generate map of clustering to original index.

    If the data frame has some holes (NaN values), they shouldn't be passed to
    clustering algorithms. But once the

    Arguments:
        df -- source data frame.

    Returns:
        Mapping of clustering result index to original data frame index.
    """
    good_row_i = 0
    hole_map: list[tuple[int, int]] = []
    for row_i, row in df.iterrows():
        assert isinstance(row_i, int), "Row index is not an integer."
        if not any(row.isna()):
            hole_map.append((good_row_i, row_i))
            good_row_i += 1
    return tuple(hole_map)


def fill_holes(
    clustered: npt.NDArray[Any],
    hole_map: HoleMap,
    fill_with: Any = math.nan,
) -> npt.NDArray[Any]:
    """Fill holes in clustering result.

    Arguments:
        clustered -- clustering result.
        hole_map -- hole map for the data frame (generated using `generate_hole_map()`).

    Keyword Arguments:
        fill_with -- value used to fill the holes with (default: {math.nan}).

    Returns:
        Clustered data with holes filled.
    """
    output = np.full(max(dst for _, dst in hole_map) + 1, fill_with)
    for src, dst in hole_map:
        output[dst] = clustered[src]
    return output
