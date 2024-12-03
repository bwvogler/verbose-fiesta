"""Look at an experiment and analyze the data."""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(
    "C:/Users/bvogler/repos/research-and-analysis/echem/data/PeakData_BDM2-6_CAL_EnzymeTitration_10cycles_4Dilutions_2024-11-19.csv"
).assign(
    Run=lambda x: x["Run"].astype(int),
    # convert letter row to number zero-indexed
    row=lambda x: x["Well"].map(lambda x: ord(x[0]) - 65),
    col=lambda x: x["Well"].map(lambda x: int(x[1:]) - 1),
    dilution=lambda x: x["Run"].map(lambda x: int((x - 1) / 10)),
    concentration=lambda x: x["dilution"].apply(lambda x: 300 / (2**x)),
)


def remove_outliers(
    df: pd.DataFrame, column: str, by: None | str | list[str] = None, p: float = 0.05
) -> pd.DataFrame:
    """Remove outliers from a DataFrame."""
    if by is None:
        by = []
    elif isinstance(by, str):
        by = [by]
    return (
        df.groupby(by)
        .apply(
            lambda x: x[
                x[column].between(x[column].quantile(p), x[column].quantile(1 - p))
            ]
        )
        .reset_index(drop=True)
    )


df_no_outliers = remove_outliers(df, "Current", by=["Well", "dilution"])


df_no_outliers[df_no_outliers["Well"] == "E5"]
df_means = (
    df_no_outliers.drop(columns="Run")
    .groupby(["Well", "dilution"])
    .mean()
    .reset_index()
)


well, well_df = next(iter(df_means.groupby("Well")))
well_df["concentration"] = well_df["concentration"].astype(float)
sns.scatterplot(data=well_df, x="concentration", y="Current")
# make x axis linear scale
plt.xscale("linear")

sns.catplot(
    data=df_no_outliers[~df_no_outliers["Well"].isin(["C6", "D9"])],
    row="row",
    col="col",
    x="dilution",
    y="Current",
    hue="Run",
    kind="point",
    height=1,
    aspect=1,
)
sns.catplot(
    data=df_means[~df_means["Well"].isin(["C6", "D9"])],
    row="row",
    col="col",
    x="concentration",
    y="Current",
    kind="point",
    height=1,
    aspect=1,
)
g = sns.FacetGrid(
    data=df_means[~df_means["Well"].isin(["C6", "D9"])],
    row="row",
    col="col",
    height=1,
    aspect=1,
)
g.map(sns.scatterplot, "concentration", "Current")

plt.show()
