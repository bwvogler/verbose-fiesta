import numpy as np
import pandas as pd

from pyquorra.platemap import Platemap, WellPosition

from lunatic import LunaticParser, unpack_annotations


lunatic_parser = LunaticParser()
parsed_data = lunatic_parser.parse(
    # "lunatic/data/2024-12-13_143852_401155_LUNA_2024-12-13_MicroBCA.xlsx"
    # "lunatic/data/2024-12-17_164941_401155_LUNA_2024-12-17_MicroBCA_left.xlsx"
    # "lunatic/data/2024-12-17_170553_401155_LUNA_2024-12-17_MicroBCA_right.xlsx"
    # "lunatic/data/2025-01-15_144936_401155_LUNA_uBCA.xlsx"
    # "lunatic/data/2025-01-15_161155_401155_LUNA_uBCA.xlsx"
    "lunatic/data/2025-01-21_112225_401155_LUNA.xlsx"
)


lunatic_data = unpack_annotations(
    pd.concat([pd.DataFrame(plate.wells) for plate in parsed_data.plates])
)


platemap = Platemap.from_quorra("G0033171")
platemap_data = unpack_annotations(pd.DataFrame(platemap.well_records))

data = pd.merge(
    lunatic_data,
    platemap_data,
    left_on=["row", "column"],
    right_on=["row", "column"],
    how="inner",
)

# add mean of columns A555-569 and A642-664
data = data.assign(
    mean_560=lambda x: x.loc[:, "555":"569"].mean(axis=1),
    mean_655=lambda x: x.loc[:, "642":"664"].mean(axis=1),
    difference=lambda x: x["mean_560"] - x["mean_655"],
)

calibration_data = data[data["control"] == "standard"]


# calculate the slope and intercept of the calibration curve (difference vs. concentration)
slope, intercept = np.polyfit(
    calibration_data["concentration"], calibration_data["difference"], 1
)

# characterize calibration curve
calibration_data = calibration_data.assign(
    calculated_conc=lambda x: (x["difference"] - intercept) / slope
)


analyzed_data = data.assign(
    concentration=lambda x: (x["difference"] - intercept) / slope
)

# analyzed_data.to_csv("lunatic/data/GOLDBTX_sizing.csv", index=False)

for well_data in analyzed_data.itertuples():
    platemap._wells[WellPosition(well_data.row, well_data.column)]["concentration"] = well_data.concentration

platemap.update_quorra()
