"""Utility functions for the echem package."""

import pandas as pd


def get_data(filepath: str) -> pd.DataFrame:
    """Read in the data and add some columns."""
    df = pd.read_csv(filepath).assign(
        Run=lambda x: x["Run"].astype(int),
        # convert letter row to number zero-indexed
        row=lambda x: x["Well"].map(lambda x: ord(x[0]) - 65),
        col=lambda x: x["Well"].map(lambda x: int(x[1:]) - 1),
    )
    return df
