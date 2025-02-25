from typing import Tuple
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.stats import linregress
import scipy.special as sp

import scipy.optimize as opt


from pyquorra.platemap import Platemap

from uv import SynergyParser
from util import PALETTE

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
                if isinstance(y, float) and not np.isnan(y) and not np.isinf(y)
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


# Perform curve fitting
def integrated_mm(t, Vmax, Km, S0):
    """Compute [S](t) using the Lambert W function solution to the integrated MM equation."""
    C = Vmax * t - S0 - Km * np.log(S0)

    # Ensure Lambert function is evaluated correctly
    W_input = -np.exp(-C / Km)

    # Prevent invalid values in W (should be between -1/e and 0)
    W_input = np.clip(W_input, -1 / np.e, 0.0)

    # Compute Lambert W function on the correct branch
    S_t = -Km * sp.lambertw(W_input, k=-1).real  # Ensure real part

    return S_t


def smooth_approximation(t, S0, Sinf, k):
    return Sinf + (S0 - Sinf) * np.exp(-k * t)


def smooth_approximation_derivative(t, S0, Sinf, k):
    return -k * (S0 - Sinf) * np.exp(-k * t)


well_df = wells_df.iloc[0]  # 218]  # 115]
well_df = wells_df.iloc[218]  # 115]
well_df = wells_df.iloc[115]

popt, pcov = opt.curve_fit(  # pylint:disable=unbalanced-tuple-unpacking
    smooth_approximation,
    *get_x_y_data(well_df, "seconds", "Adjusted 292"),
    p0=[max(well_df["Adjusted 292"]), min(well_df["Adjusted 292"]), 0.00001],
    bounds=([0, 0, 0], [5, 5, 1]),
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

well_df = wells_df.iloc[218]  # 115]
wells_df["popt"] = [
    opt.curve_fit(
        smooth_approximation,
        *get_x_y_data(well_df, "seconds", "Adjusted 292"),
        p0=[max(well_df["Adjusted 292"]), min(well_df["Adjusted 292"]), 0.00001],
        bounds=([0, 0, 0], [5, 5, 1]),
    )[0]
    # opt.curve_fit(
    #     integrated_mm,
    #     *get_x_y_data(well_df, "seconds", "Adjusted 292"),
    #     p0=[0.001, 50.0, 0.00001],
    #     bounds=([0, 0, 0], [5, 500, 10]),
    # )[0]
    for well_df in wells_df.iloc()
]

wells_df["max_d Adjusted 292"] = [
    smooth_approximation_derivative(
        0,
        *list(
            opt.curve_fit(
                smooth_approximation,
                *get_x_y_data(well_df, "seconds", "Adjusted 292"),
                p0=[
                    max(well_df["Adjusted 292"]),
                    min(well_df["Adjusted 292"]),
                    0.00001,
                ],
                bounds=([0, 0, 0], [5, 5, 1]),
            )[0]
        ),
    )
    for well_df in wells_df.iloc()
]

wells_df["Vmax"] = wells_df["max_d Adjusted 292"] / standard_curve.slope

# investigate limit of quantification
negative_df = wells_df[
    (wells_df["enzymeconcentration"] == 0) & (wells_df["control"] == "standard")
]

mean_Vmax = negative_df["Vmax"].mean()
std_Vmax = negative_df["Vmax"].std()
lod = mean_Vmax - 3 * std_Vmax

# calculate the Vmax for each enzymeconcentration
rough_data = (
    wells_df.groupby("enzymeconcentration")
    .aggregate(
        {
            "Vmax": ["mean", "std"],
        }
    )
    .reset_index()
)

rough_data["enzymenm"] = 1000 * rough_data["enzymeconcentration"] / 5 / 35
rough_data["kcat"]

# plot curves for each enzyme concentration
x = np.linspace(0, max(x for y in wells_df["seconds"] for x in y), 100)
long_data = pd.concat(
    [
        pd.DataFrame(
            data=np.array(get_x_y_data(well_df, "seconds", "Adjusted 292")).T,
            columns=["seconds", "Adjusted 292"],
        ).assign(
            enzymeconcentration=well_df["enzymeconcentration"],
            well=well_df["well_location"],
            smooth=lambda x, well_df=well_df: smooth_approximation(
                x["seconds"], *well_df["popt"]
            ),
        )
        for well_df in wells_df.iloc()
        if well_df["enzymeconcentration"] > 0
    ]
)

sns.scatterplot(
    data=long_data,
    x="seconds",
    y="Adjusted 292",
    hue="enzymeconcentration",
    palette=PALETTE,
)
sns.lineplot(
    data=long_data,
    x="seconds",
    y="smooth",
    hue="enzymeconcentration",
    legend=False,
    palette=PALETTE,
)
plt.show()

# look for trends in error
long_data["error"] = long_data["Adjusted 292"] - long_data["smooth"]
long_data[
    long_data["enzymeconcentration"].isin(
        list(long_data["enzymeconcentration"].unique())[:3]
    )
].plot(
    x="seconds",
    y="error",
    kind="scatter",
    marker="o",
    c="enzymeconcentration",
    s=3,
    cmap=ListedColormap(PALETTE),
)
plt.show()
