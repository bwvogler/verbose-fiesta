"""Analyze the fluorescence polarization data"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_data():
    """Load the fluorescence polarization data"""
    data = pd.read_csv(
        "fluorescent_polarization/data/20241204 FP.csv",
        names=["sample", "well", "parallel", "perpendicular", "pol"],
        skiprows=1,
    ).assign(
        F=lambda x: x["parallel"] + x["perpendicular"],
    )
    return data


def get_figure_size(location: str = "side", exclude_title: bool = False) -> tuple:
    """
    Return predefined figure sizes based on location and title inclusion.

    Args:
        location (str): 'side' or 'whole'. Default is 'side'.
        exclude_title (bool): If True, reduce height by 0.61 inches. Default is False.

    Returns:
        tuple: (height, width) in inches
    """
    sizes = {
        "side": (5.5, 7.35),
        "whole": (5.5, 12.3),
    }
    height, width = sizes.get(location, sizes["side"])
    if exclude_title:
        height -= 0.61
    return (height, width)


def setup_seaborn_theme(location: str = "side", exclude_title: bool = False):
    """Set up standard Seaborn theme for figures with predefined sizes."""
    palette = [
        "#51A4AF",  # Medium Teal
        "#71257D",  # Dark Purple
        "#F8AE35",  # Medium Orange
        "#125F69",  # Dark Teal
        "#D36DB6",  # Medium Purple
        "#DD8411",  # Dark Orange
        "#98D6D7",  # Light Teal
        "#F9B7E7",  # Light Purple
        "#FBCC7E",  # Light Orange
    ]
    sns.set_theme(style="white", palette=palette)
    # make the background of the figure transparent, but the axes white
    plt.rcParams["figure.facecolor"] = "none"
    plt.rcParams["axes.facecolor"] = "white"
    sns.set_context("talk", font_scale=1.2)
    plt.rcParams["figure.figsize"] = get_figure_size(location, exclude_title)
    plt.rcParams["font.family"] = "Arial"
    # only include major gridlines for y-axis
    plt.rcParams["grid.linestyle"] = "-"
    plt.rcParams["grid.linewidth"] = 2
    plt.rcParams["grid.color"] = "lightgray"
    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.grid.axis"] = "y"
    plt.rcParams["axes.grid.which"] = "major"
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.titleweight"] = "bold"


setup_seaborn_theme()
df = get_data().assign(F_10K=lambda x: x["F"] / 10000)
g = sns.catplot(
    data=df,
    x="ph",
    y="F_10K",
    hue="enzyme",
    col="inhibitor",
    kind="box",
    col_wrap=4,
    sharey=True,
    # hide outliers for clarity
    showfliers=False,
    aspect=1 / len(df["inhibitor"].unique()),
)
g.set_axis_labels("", "Fluorescence (10K)")
g.set_titles("{col_name}")
for ax in g.axes.flat:
    ax.label_outer()
    if ax.get_subplotspec().colspan.start != 0:
        # Remove y-axis line for all but the first column
        ax.spines["left"].set_visible(False)
plt.tight_layout(w_pad=0)
# plot the legend in the top left
g.legend.set_bbox_to_anchor([0.5, 0.6], transform=g.figure.transFigure)
# give the legend a white background so the gridlines aren't visible behind it
g.legend.get_frame().set_facecolor("white")
plt.savefig("fluorescent_polarization/charts/figure_five.svg")


def figure_two(location: str = "side", exclude_title: bool = False):
    """Demonstrate the impact of pH and enzyme on the fluorescence polarization of each inhibitor"""
    setup_seaborn_theme(location, exclude_title)
    df = get_data()
    # remove none inhibitor
    df = df[df["F"] > 1000]
    # plot categorical scatters with each point alpha being the F value
    g = sns.catplot(
        data=df,
        x="ph",
        y="pol",
        hue="enzyme",
        col="inhibitor",
        # row="urate",
        kind="box",
        sharey=True,
        showfliers=False,
        aspect=1 / len(df["inhibitor"].unique()),
    )
    g.set_axis_labels("", "Fluorescence Polarization (mP)")
    g.set_titles("{col_name}")
    for ax in g.axes.flat:
        ax.label_outer()
        if ax.get_subplotspec().colspan.start != 0:
            # Remove y-axis line for all but the first column
            ax.spines["left"].set_visible(False)
    plt.tight_layout(w_pad=0)
    plt.savefig("fluorescent_polarization/charts/figure_two.svg")


def figure_three(location: str = "side", exclude_title: bool = False):
    """Demonstrate the impact of pH and enzyme on the fluorescence polarization of each inhibitor"""
    setup_seaborn_theme(location, exclude_title)
    df = get_data()
    # investigate the impact of ph and enzyme on the uv
    g = sns.catplot(
        data=df,
        x="ph",
        y="uv",
        hue="enzyme",
        col="inhibitor",
        row="urate",
        kind="box",
        sharey=True,
        showfliers=False,
        aspect=len(df["urate"].unique()) / len(df["inhibitor"].unique()),
        height=plt.rcParams["figure.figsize"][1] / len(df["urate"].unique()),
    )
    g.set_axis_labels("", "OD292")
    g.set_titles("{col_name}")
    for ax in g.axes.flat:
        if ax.get_subplotspec().is_first_row():
            ax.set_title(ax.get_title())
        else:
            ax.set_title("")
    for ax in g.axes.flat:
        ax.label_outer()
        if ax.get_subplotspec().colspan.start != 0:
            # Remove y-axis line for all but the first column
            ax.spines["left"].set_visible(False)
    # put the legend in the right plot of the top row
    g.legend.set_bbox_to_anchor([0.75, 0.75], transform=g.figure.transFigure)

    plt.tight_layout(w_pad=0)
    plt.savefig("fluorescent_polarization/charts/figure_three.svg")


def figure_four(location: str = "side", exclude_title: bool = False):
    setup_seaborn_theme(location, exclude_title)
    df = get_data()
    df = df[df["urate"] == "Yes"]
    # investigate the impact of ph and enzyme on the uv
    g = sns.catplot(
        data=df,
        x="ph",
        y="uv_norm",
        hue="enzyme",
        col="inhibitor",
        kind="box",
        sharey=True,
        legend_out=True,
        showfliers=False,
        aspect=1 / len(df["inhibitor"].unique()),
    )
    g.set_axis_labels("", "OD292 - background")
    g.set_titles("{col_name}")
    for ax in g.axes.flat:
        ax.label_outer()
        if ax.get_subplotspec().colspan.start != 0:
            # Remove y-axis line for all but the first column
            ax.spines["left"].set_visible(False)
    # give the legend a white background so the gridlines aren't visible behind it
    g.legend.set_bbox_to_anchor([0.85, 0.45], transform=g.figure.transFigure)
    g.legend.get_frame().set_facecolor("white")

    plt.tight_layout(w_pad=0)
    plt.savefig("fluorescent_polarization/charts/figure_four.svg")


figure_one()
figure_two()
figure_three()
figure_four()
