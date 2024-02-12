"""Tools used to convert raw data from nanoindenter to a data frame."""

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile

from metale_amorficzne.utils import DEFAULT_COLUMNS

REQUIRED_COLUMNS = ("X [mm]", "Y [mm]", *DEFAULT_COLUMNS)
"""Required columns in source file to perform the default analysis."""


def convert_raw_to_df(
    raw_input: Path | str | UploadedFile, sort_x_y: bool = False
) -> pd.DataFrame:
    """Convert raw file from nanoindenter to a data frame.

    Arguments:
        raw_input -- either a path to the source file or UploadedFile from Streamlit.
        sort_x_y -- sort data frame by X and Y coordinates.

    Raises:
        ValueError: error during parsing.

    Returns:
        Data frame with parsed data.
    """
    if not isinstance(raw_input, UploadedFile):
        print(f"Parsing {raw_input}")

    df = pd.DataFrame()

    with (
        raw_input if isinstance(raw_input, UploadedFile) else open(raw_input, "rb")
    ) as raw_file:
        if [raw_file.readline().strip() for _ in range(3)] != [
            b"",
            b"New Report",
            b"----------",
        ]:
            raise ValueError("File header is not valid")

        df.Name = raw_file.readline().strip().decode("utf8")

        column_name = ""
        data: dict[int, float | None] = {}
        for line in raw_file.readlines():
            line = line.decode("utf8")

            row = line.split("\t")
            if len(row) < 3:
                # Ignore empty lines.
                continue

            if row[0] != "" and not row[0].startswith("["):
                # Section header

                if any(isinstance(element, float) for element in data.values()):
                    # Save current column to data frame if the column has any values.
                    data_list = np.full(max(data.keys()), math.nan)
                    for i, value in data.items():
                        data_list[i - 1] = value
                    df[column_name] = data_list

                # Initialize new section.
                data = {}
                column_name = row[0]
            elif row[0] != "":
                # Section header unit
                column_name += " " + row[0]

            if not row[1].startswith("Data"):
                # Ignore statistics at the end of column.
                continue

            data[int(row[1].split(" : ")[1])] = (
                float(row[2].replace(",", ".")) if row[2] != "--.--" else None
            )

    # Postprocessing
    ## Ensure data has all the required columns.
    missing_columns = [
        column_name for column_name in REQUIRED_COLUMNS if column_name not in df.columns
    ]
    if len(missing_columns) > 0:
        raise ValueError(
            "Input data doesn't contain required columns: " + ", ".join(missing_columns)
        )

    if sort_x_y:
        ## Ensure data points are in order.
        df.sort_values(["Y [mm]", "X [mm]"], inplace=True)

    ## Check if we can make a square out of the data frame (for visualization).
    square = math.sqrt(len(df))
    if square != int(square):
        raise ValueError("Input data frame is not square.")

    return df


def convert_single_file(input_path: Path, output_path: Path):
    """Convert a single file from raw data to a CSV.

    Arguments:
        input_path -- path to the input raw file.
        output_path -- path to the output CSV file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise RuntimeError(f"The input path does not exist: {input_path}")

    df = convert_raw_to_df(input_path)
    print(f"Saving the data to {output_path}.")
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong number of arguments. Expected format: INPUT_DIR OUTPUT_DIR")
        sys.exit(1)

    input_dir, output_dir = Path(sys.argv[1]), Path(sys.argv[2])
    if not input_dir.is_dir() or not input_dir.exists():
        print("Input directory is not a directory or doesn't exist")
        sys.exit(1)

    for input_file in input_dir.rglob("**/*.TXT"):
        if input_file.is_dir() or input_file.parent.name.endswith("_curves"):
            continue

        convert_single_file(
            input_file,
            (output_dir / input_file.relative_to(input_dir)).with_suffix(".csv"),
        )
