import pandas as pd
from echem.calibration import get_calibration_data
from util import setup_seaborn_theme

df = get_calibration_data("echem/data/three_cals.csv").assign(# convert run to int and take the 10 modulus
    Run=lambda x: x["Run"].astype(int) % 10
)
df = df[
    (df["Run"] > 2)
    & (df["Well"] < "C6")
    & (df["Well"] != "D9")
]

(well, concentration), data = next(
    iter(df[df["concentration"] != 0].groupby(["Well", "concentration"]))
)
# get the std of the change in value for each calibration run
calibration_slope_stds = pd.concat(
    [
        pd.Series(
            dict(
                **{"Well": well, "concentration": concentration},
                **dict(
                    # (10**9)*
                    data.sort_values("Run")
                    .iloc[:, data.columns.str.startswith("Cal")]
                    .diff()
                    .std()
                ),
            ),
            # dtype=float
        )
        for (well, concentration), data in df[(df["concentration"] != 0)].groupby(
            ["Well", "concentration"]
        )
    ],
    axis=1,
    ignore_index=True,
).T
calibration_slope_stds.columns = ["Well", "concentration", "Cal 1", "Cal2", "Cal3"]
calibration_slope_stds = calibration_slope_stds.melt(
    id_vars=["Well", "concentration"],
    value_vars=["Cal 1", "Cal2", "Cal3"],
    var_name="Cal",
    value_name="slope_std",
)
# replace values greater than 100 with 100
calibration_slope_stds["slope_std"] = calibration_slope_stds["slope_std"].clip(
    upper=0.5 * 10**-7
)

# plot histograms of these stds colored by Cal number
import seaborn as sns
import matplotlib.pyplot as plt

setup_seaborn_theme()
# get size of current figure
fig_size = plt.gcf().get_size_inches()
# close the current figure
plt.close()
# make a FacetGrid of the histograms with a legend
g = sns.FacetGrid(
    calibration_slope_stds,
    col="Cal",
    col_wrap=2,
    sharex=True,
    sharey=True,
    hue="concentration",
)
g.map(sns.histplot, "slope_std", kde=True, binrange=(0, 0.5 * 10**-7), bins=50)

# Add legend to the FacetGrid, bottom right position
g.add_legend(title="Concentration", loc="center", bbox_to_anchor=(0.6, 0.25))

plt.gcf().set_size_inches(fig_size)
# change the titles
g.set_titles("Calibration {col_name}")
plt.show()


# identify the worst concentration/well combinations and plot their normalized traces
first, second = (5, 10)
worst = list(
    calibration_slope_stds.sort_values("slope_std", ascending=False)
    .head(first + second)[["Cal", "Well", "concentration"]]
    .tail(second)
    .itertuples(index=False, name=None)
)
melted_data = df.melt(
    id_vars=["Run", "Well", "concentration"],
    value_vars=data.columns[data.columns.str.startswith("Cal")],
    var_name="Cal",
    value_name="Current",
)
grouped_data = melted_data.groupby(["Cal", "Well", "concentration"])
norm_worst = pd.concat([
    grouped_data.get_group((cal_no, well, concentration)).assign(
        Current=lambda x: x["Current"] - x["Current"].mean(),
        identifier=f"{cal_no} {well} {concentration}"
    )
    for cal_no, well, concentration in worst
])

# plot the normalized traces all on one plot, colored by (Cal, concentration, well)
sns.lineplot(
    data=norm_worst,
    x="Run",
    y="Current",
    hue="identifier",
    palette="viridis",
)
plt.show()

