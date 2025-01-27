import seaborn as sns
import matplotlib.pyplot as plt

PALETTE = [
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

    sns.set_theme(style="white", palette=PALETTE)
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
