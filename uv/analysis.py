from typing import Tuple
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress

import scipy.optimize as opt
import scipy.special as sp


from pyquorra.platemap import Platemap

from uv import SynergyParser

parser = SynergyParser()

parsed_data = parser.parse("uv/data/UV serum.xlsx")

parsed_df = pd.DataFrame(parsed_data.plates[0].wells)
parsed_data_df = pd.concat(
    [
        parsed_df.drop(columns=["annotations"]),
        pd.json_normalize(parsed_df["annotations"]),
    ],
    axis=1,
)

platemap = Platemap.from_quorra("G0033941")
platemap_df = pd.DataFrame(platemap.well_records)
# unpack annotations column jsons
well_annotations_df = pd.concat(
    [
        platemap_df.drop(columns=["annotations"]),
        pd.json_normalize(platemap_df["annotations"]),
    ],
    axis=1,
)

wells_df = pd.merge(
    parsed_data_df,
    well_annotations_df,
    on=["row", "column"],
    how="inner",
)

standards_df = wells_df[wells_df["control"] == "standard"]


# perform a linear regression on the adjusted 292 vs time to calculate the y intercept (value at t=0)
def get_x_y_data(
    df: pd.DataFrame, x_col: str, y_col: str, data_slice: slice = slice(None, None)
) -> Tuple[list[float], list[float]]:
    x, y = tuple(
        zip(
            *[
                (x, y)
                for x, y in zip(df[x_col], df[y_col])
                if isinstance(y, float) and not np.isnan(y)
            ]
        )
    )
    return x[data_slice], y[data_slice]


standards_df["y_intercept"] = [
    linregress(*get_x_y_data(well_df, "time", "Adjusted 292")).intercept
    for well_df in standards_df.iloc()
]

standard_curve = linregress(
    standards_df["uricacidconcentration"], standards_df["y_intercept"]
)

standards_df["uric_acid_concentration"] = standards_df["y_intercept"].apply(
    lambda y_intercept: (y_intercept - standard_curve.intercept)
    / standard_curve.slope
    # lambda y_intercept: standard_curve.intercept + standard_curve.slope * y_intercept
)

sns.scatterplot(
    data=standards_df,
    x="uricacidconcentration",
    y="uric_acid_concentration",
)
plt.show()


def apply_standard_curve(
    input_list: list[float],
    std_curve,
) -> list[float]:
    input_array = np.array(
        input_list, dtype=np.float64
    )  # Ensure the input is a float64 array
    return np.where(
        np.isnan(input_array),
        np.nan,
        (np.array(input_array) - std_curve.intercept) / std_curve.slope,
    ).tolist()


wells_df["calculatedconcentration"] = wells_df["Adjusted 292"].apply(
    lambda x: (np.array(x) - standard_curve.intercept)
    / standard_curve.slope
    # apply_standard_curve, args=(standard_curve,)
)

wells_df["seconds"] = wells_df["time"].apply(lambda x: list(24 * 60 * 60 * np.array(x)))


# Define the integrated Michaelis-Menten equation solved for S
def integrated_mm(t, Vmax, Km, S0):
    """Compute [S](t) using the Lambert W function solution to the integrated MM equation."""
    C = Vmax * t - S0 - Km * np.log(S0)
    S_t = -Km * sp.lambertw(-np.exp(-C / Km), k=-1).real  # Ensure real part
    return S_t


# Perform curve fitting


def smooth_approximation(t, S0, Sinf, k):
    return Sinf + (S0 - Sinf) * np.exp(-k * t)


well_df = wells_df.iloc[0]  # 115]
# popt, pcov = opt.curve_fit(
#     integrated_mm,
#     *get_x_y_data(well_df, "seconds", "calculatedconcentration", slice(0, 25)),
#     p0=[1.0, 30.0, 300.0],
#     bounds=([0, 0, 0], [np.inf, np.inf, 500])
# )
popt, pcov = opt.curve_fit(
    smooth_approximation,
    *get_x_y_data(well_df, "seconds", "Adjusted 292"),
    p0=[max(well_df["Adjusted 292"]), min(well_df["Adjusted 292"]), 0.1],
    bounds=([0, 0, 0], [np.inf, np.inf, 500])
)
# plot a fit
x = np.linspace(min(well_df["seconds"]), max(well_df["seconds"]), 100)
# y = integrated_mm(x, *popt)
y = smooth_approximation(x, *popt)
plt.plot(x, y, label="Fitted curve")
plt.scatter(
    *get_x_y_data(well_df, "seconds", "Adjusted 292"), label="Data"  # , slice(0, 25)),
)
plt.show()
# plt.close()


def get_dy_data(row: pd.Series, x_col: str, y_col: str) -> list[float]:
    """Get the derivative of the y data. With respect to x. Return dY with the same length as x and spaced as y."""
    dy = [np.nan]
    last_x_y: Tuple[float, float] = (np.nan, np.nan)
    for x, y in zip(row[x_col], row[y_col]):
        if isinstance(y, float) and not np.isnan(y):
            if last_x_y != (np.nan, np.nan):
                dy.append((y - last_x_y[1]) / (x - last_x_y[0]))
            last_x_y = (x, y)
        else:
            dy.append(np.nan)
    return dy


wells_df["d Adjusted 292"] = wells_df.apply(
    lambda row: get_dy_data(row, "seconds", "Adjusted 292"), axis=1
)

wells_df["d calculatedconcentration"] = wells_df["d Adjusted 292"].apply(
    lambda x: np.array(x) / standard_curve.slope
)


def mm_deriv(t, Vmax, Km, S0):
    """Compute d[S](t)/dt using the Lambert W function solution to the integrated MM equation."""
    C = Vmax * t - S0 - Km * np.log(S0)
    dS_dt = -Vmax / (1 + S0 / Km) * np.exp(-C / Km)
    return dS_dt


popt, pcov = opt.curve_fit(
    mm_deriv,
    *get_x_y_data(well_df, "seconds", "d calculatedconcentration", slice(0, 25)),
    p0=[1.0, 30.0, 300.0],
    bounds=([0, 0, 0], [np.inf, np.inf, 500])
)
# plot a fit
x = np.linspace(min(well_df["seconds"]), max(well_df["seconds"]), 100)
y = mm_deriv(x, *popt)
plt.plot(x, y, label="Fitted curve")
plt.scatter(
    *get_x_y_data(well_df, "seconds", "d calculatedconcentration", slice(0, 25)),
    label="Data"
)
plt.show()
plt.close()
