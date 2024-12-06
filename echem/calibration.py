"""Look at an experiment and analyze the data."""

import pandas as pd
import numpy as np
from echem.util import get_data
from scipy.stats import linregress
import matplotlib.pyplot as plt


def get_calibration_data(
    filepath: str,
    runs_each: int = 10,
    start_conc: float = 300,
    dil_factor: float = 2,
    lowest_zero: bool = True,
) -> pd.DataFrame:
    """Read in the data and add some columns."""
    df = get_data(filepath).assign(
        dilution=lambda x: x["Run"].map(lambda x: int((x - 1) / runs_each)),
        concentration=lambda x: x["dilution"].apply(
            lambda x: start_conc / (dil_factor**x)
        ),
    )
    if lowest_zero:
        lowest_conc = df["concentration"].min()
        df["concentration"] = df.apply(
            lambda x: 0 if x["concentration"] == lowest_conc else x["concentration"],
            axis=1,
        )
    return df


def remove_outliers(
    df: pd.DataFrame, column: str, by: None | str | list[str] = None, p: float = 0.05
) -> pd.DataFrame:
    """Remove outliers from a DataFrame."""
    if by is None:
        by = []
    elif isinstance(by, str):
        by = [by]
    return (
        df.groupby(by)[df.columns]
        .apply(
            lambda x: x[
                x[column].between(x[column].quantile(p), x[column].quantile(1 - p))
            ],
        )
        .reset_index(drop=True)
    )


def get_linear_fit(df: pd.DataFrame) -> pd.DataFrame:
    """Get linear fit for each well."""
    fits = df.groupby("Well")[df.columns].apply(
        lambda x: pd.Series(
            linregress(x["concentration"], x["Current"]),
            index=["slope", "intercept", "r_value", "p_value", "std_err"],
        )
    )
    return fits.reset_index().assign(r_squared=lambda x: x["r_value"] ** 2)


def plot_fit(df: pd.DataFrame, fits: pd.DataFrame, well: str) -> None:
    """Plot the fit for a given well."""
    coeffs = fits.set_index("Well").loc[well]
    x = np.linspace(0, 300, 100)
    y = coeffs["slope"] * x + coeffs["intercept"]
    df_well = df[df["Well"] == well]
    df_well.plot(x="concentration", y="Current", kind="scatter")
    plt.plot(x, y, c="r")
    plt.title(f"Well {well}")
    plt.show()


def get_calibration(filepath: str) -> pd.DataFrame:
    """Get the calibration data for an experiment."""
    df = get_calibration_data(filepath)
    df_no_outliers = remove_outliers(df, "Current", by=["Well", "dilution"])
    df_means = (
        df_no_outliers.drop(columns="Run")
        .groupby(["Well", "dilution"])
        .mean()
        .reset_index()
    )
    df_fits = get_linear_fit(df_means)
    return df_fits


def get_quadratic_fit(df: pd.DataFrame) -> pd.DataFrame:
    """Get quadratic fit for each well."""

    def fit_quadratic(
        data: pd.Series, x: str = "concentration", y: str = "Current"
    ) -> pd.Series:
        coeffs = np.polyfit(data[x], data[y], 2)
        return pd.Series(
            {
                "a": coeffs[0],
                "b": coeffs[1],
                "c": coeffs[2],
            }
        )

    fits = df.groupby("Well")[df.columns].apply(fit_quadratic).reset_index()
    coeffs = {x[0]: tuple(x[1:]) for x in (fits.itertuples(name=None, index=False))}
    df["pred"] = df.apply(
        lambda x: np.polyval(coeffs[x["Well"]], x["concentration"]), axis=1
    )
    df["residual"] = df["Current"] - df["pred"]
    df["residuals_squared"] = df["residual"] ** 2
    r_squares = {
        well: (
            1
            - well_df["residuals_squared"].sum()
            / (well_df["Current"] - well_df["Current"].mean())
            .apply(lambda x: x**2)
            .sum()
            if (well_df["Current"] - well_df["Current"].mean()).sum() != 0
            else np.nan
        )
        for well, well_df in df.groupby("Well")
    }
    fits["r_squared"] = fits["Well"].map(r_squares)

    return fits
