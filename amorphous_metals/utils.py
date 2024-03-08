"""Miscellaneous data frame analysis utilities."""

import math
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd

DEFAULT_COLUMNS = (
    "HIT (O&P) [MPa]",
    "HVIT (O&P) [Vickers]",
    "EIT (O&P) [GPa]",
    "nit [%]",
)
"""Default columns used for clustering."""


def image_width(df: pd.DataFrame) -> int:
    """Get (square) image width for the given data frame.

    Arguments:
        df -- source data frame.

    Returns:
        Width/height of the resulting square image.
    """
    return int(math.sqrt(len(df)))


def has_holes(df: pd.DataFrame) -> tuple[bool, ...]:
    """Check if data frame has data holes.

    Arguments:
        df -- source data frame.

    Returns:
        If a row has a hole, the value is True.
    """
    return tuple(df.isnull().any(axis=1))


def filter_holes(df: pd.DataFrame) -> pd.DataFrame:
    """Filter out data holes from data frame.

    Arguments:
        df -- source data frame.

    Returns:
        Data frame without data holes.
    """
    return df[~df.isnull().any(axis=1)]


def generate_hole_map(df: pd.DataFrame) -> tuple[int, ...]:
    """Generate map of clustering to original index.

    If the data frame has some holes (NaN values), they shouldn't be passed to
    clustering algorithms. But once the

    Arguments:
        df -- source data frame.

    Returns:
        Mapping of clustering result index to original data frame index.
    """
    return tuple(row_i for row_i, row in df.iterrows() if not any(row.isnull()))  # type: ignore


def fill_holes(
    source_df: pd.DataFrame,
    clustered: npt.NDArray[Any],
    fill_with: Any = math.nan,
) -> npt.NDArray[Any]:
    """Fill holes in clustering result.

    Arguments:
        source_df -- source data frame (with holes).
        clustered -- clustering result.

    Keyword Arguments:
        fill_with -- value used to fill the holes with (default: {math.nan}).

    Returns:
        Clustered data with holes filled.
    """
    output = [fill_with for _ in range(len(source_df))]
    for src, dst in enumerate(generate_hole_map(source_df)):
        output[dst] = clustered[src]
    return np.array(output)
