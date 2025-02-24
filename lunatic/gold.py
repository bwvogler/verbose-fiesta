import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pyquorra.platemap import PlatemapList, WellPosition

from lunatic import LunaticParser, unpack_annotations
from util import PALETTE


file_plate_pairings = {
    # "lunatic/data/2024-12-13_143852_401155_LUNA_2024-12-13_MicroBCA.xlsx"
    # "lunatic/data/2024-12-17_164941_401155_LUNA_2024-12-17_MicroBCA_left.xlsx"
    # "lunatic/data/2024-12-17_170553_401155_LUNA_2024-12-17_MicroBCA_right.xlsx"
    # "lunatic/data/2025-01-15_144936_401155_LUNA_uBCA.xlsx"
    # "lunatic/data/2025-01-15_161155_401155_LUNA_uBCA.xlsx"
    # "G0033171": "lunatic/data/2025-01-21_112225_401155_LUNA.xlsx",
    # "G0033294": "lunatic/data/2025-01-24_171715_401155_LUNA_2025-01-24_Micro_BCA.xlsx",
    # "G0033355": "lunatic/data/2025-01-28_162443_401155_LUNA_2025-01-28_Micro_BCA.xlsx",
    # "G0033458": "lunatic/data/2025-01-30_124501_401155_LUNA.xlsx",
    # "G0033887": "lunatic/data/2025-02-12_173500_401027_LUNA_2025-02-12_Micro_BCA_left.xlsx",  # The first plate
    # "G0033883": "lunatic/data/2025-02-12_174629_401027_LUNA_2025-02-12_Micro_BCA_right.xlsx",  # The second plate
    # "G0033966": "lunatic/data/2025-02-18_162550_401155_LUNA_Gold_Gen1_Batch1_Plate1.xlsx",  # The first plate
    # "G0033967": "lunatic/data/2025-02-18_164225_401155_LUNA_Gold_Gen1_Batch1_Plate2.xlsx",  # The second plate
    # "G0033968": "lunatic/data/2025-02-18_165551_401155_LUNA_Gold_Gen1_Batch1_Plate3.xlsx",  # The third plate
    # "G0034083": "lunatic/data/2025-02-19_160726_401155_LUNA_uBCA_Gold_Gen1_Batch2_Pla.xlsx",  # The first plate
    # "G0034084": "lunatic/data/2025-02-19_160920_401027_LUNA_uBCA_Gold_Gen1_Batch2_Pla.xlsx",
    # "G0034085": "lunatic/data/2025-02-19_162223_401155_LUNA_uBCA_Gold_Gen1_Batch2_Pla.xlsx",
    "G0034198": "lunatic/data/2025-02-21_171258_401155_LUNA_2025-02-21_MicroBCA.xlsx"
}


lunatic_parser = LunaticParser()
parsed_data = {
    plate_id: lunatic_parser.parse(file_path)
    for plate_id, file_path in file_plate_pairings.items()
}
# parsed_data["G0033458"].plates[0].wells  # for testing


lunatic_data = {
    plate_id: unpack_annotations(
        pd.concat(
            [pd.DataFrame(plate.wells) for plate in plate_data.plates]
        )  # Note: there is only ever one plate
    )
    for plate_id, plate_data in parsed_data.items()
}


platemaps = PlatemapList.from_quorra(list(lunatic_data.keys()))
platemap_data = {
    platemap.id: unpack_annotations(pd.DataFrame(platemap.well_records))
    for platemap in platemaps
}


data = pd.concat(
    [
        pd.merge(
            lunatic_data[plate_id],
            platemap_data[plate_id],
            left_on=["row", "column"],
            right_on=["row", "column"],
            how="inner",
        )
        for plate_id in file_plate_pairings.keys()
    ]
)

# add mean of columns A555-569 and A642-664
data = data.assign(
    mean_560=lambda x: x.loc[:, "555":"569"].mean(axis=1),
    mean_655=lambda x: x.loc[:, "642":"664"].mean(axis=1),
    difference=lambda x: x["mean_560"] - x["mean_655"],
)


def get_limit_of_quantitation(
    df: pd.DataFrame, signal_column: str = "difference"
) -> float:
    """Calculate the limit of quantitation for a given dataframe."""
    blanks = df[df["control"] == "blank"]
    if blanks.empty:
        blanks = df[(df["control"] == "standard") & (df["concentration"] == 0)]
    return blanks[signal_column].mean() + 10 * blanks[signal_column].std()


calibration_data = data[data["control"].isin(["standard", "blank"])]
limit_of_quantitation_signal = get_limit_of_quantitation(calibration_data)


def get_slope_intercept(
    df: pd.DataFrame,
    x_column: str = "concentration",
    y_column: str = "difference",
    y_threshold: float = -np.inf,
) -> tuple:
    """Calculate the slope and intercept of a calibration curve."""
    df_over_threshold = df[df[y_column] > y_threshold]
    return np.polyfit(
        df_over_threshold[x_column],
        df_over_threshold[y_column],
        1,
    )


slope, intercept = get_slope_intercept(
    calibration_data,  # y_threshold=limit_of_quantitation_signal
)

# characterize calibration curve
calibration_data["calculated_conc"] = (
    calibration_data["difference"] - intercept
) / slope

limit_of_quantitation = (limit_of_quantitation_signal - intercept) / slope

# plot calibration data
axes = (
    calibration_data.assign(calibration=lambda x: x["concentration"])
    .sort_values("concentration")
    .plot(
        x="concentration",
        y="calibration",
        kind="line",
        linestyle="--",
        c="black",
        label="Calibration",
    )
)
# add a horizontal line at the limit of detection
axes.axhline(limit_of_quantitation, linestyle="--", c="red", label="LoQ")

for i, (platemap_id, plate_data) in enumerate(calibration_data.groupby("platemap")):
    plate_data.plot(
        x="concentration",
        y="calculated_conc",
        kind="scatter",
        c=PALETTE[i],
        ax=axes,
        label=platemap_id,
    )
axes.set_xlabel("Concentration (ug/mL)")
axes.set_ylabel("Calculated Concentration (ug/mL)")
axes.title(
    f"Calibration Curve{"s" if len(calibration_data["platemap"].unique()) > 1 else ''}"
)
plt.legend()
plt.savefig("lunatic/data/calibration_yang.png")


analyzed_data = data.assign(
    calculated_conc=lambda x: np.where(
        True,
        # x["difference"] >= limit_of_quantitation_signal,
        (x["difference"] - intercept) / slope,
        np.nan,
    )
)

# analyzed_data.to_csv("lunatic/data/RIGHT.csv", index=False)

for platemap in platemaps:
    this_platemap_analyzed_data = analyzed_data[
        analyzed_data["platemap"] == platemap.id
    ]
    for well_data in this_platemap_analyzed_data.itertuples():
        platemap._wells[WellPosition(well_data.row, well_data.column)][
            "concentration"
        ] = well_data.calculated_conc

new_records = []
for platemap in platemaps:
    new_records.extend(platemap._update_well_records())
platemap
[platemap.id for platemap in platemaps]
