from lunatic import LunaticParser, unpack_annotations

import pandas as pd
import numpy as np


# CAL_COLUMNS = [3, 4, 5]
CAL_COLUMNS = [6, 7, 8]
HIGH_STANDARD = 180
STANDARD_DILUTION = 1.5

lunatic_parser = LunaticParser()
parsed_data = lunatic_parser.parse(
    # "lunatic/data/2024-12-13_143852_401155_LUNA_2024-12-13_MicroBCA.xlsx"
    "lunatic/data/2024-12-17_164941_401155_LUNA_2024-12-17_MicroBCA_left.xlsx"
    # "lunatic/data/2024-12-17_170553_401155_LUNA_2024-12-17_MicroBCA_right.xlsx"
    # "lunatic/data/2025-01-15_144936_401155_LUNA_uBCA.xlsx"
    # "lunatic/data/2025-01-15_161155_401155_LUNA_uBCA.xlsx"
    # "lunatic/data/2025-01-21_112225_401155_LUNA.xlsx"
)
data = unpack_annotations(
    pd.concat([pd.DataFrame(plate.wells) for plate in parsed_data.plates])
)


analyzed_data = data.assign(
    # mean of columns A555-569
    mean_560=lambda x: x.loc[:, "555":"569"].mean(axis=1),
    mean_655=lambda x: x.loc[:, "642":"664"].mean(axis=1),
    difference=lambda x: x["mean_560"] - x["mean_655"],
)

calibration_data = analyzed_data[analyzed_data["column"].isin(CAL_COLUMNS)].assign(
    conc=lambda x: x["row"].apply(lambda x: HIGH_STANDARD * STANDARD_DILUTION ** (-x))
)
calibration_data.iloc[calibration_data["row"] == max(calibration_data["row"]), -1] = 0.0
# calculate the slope and intercept of the calibration curve (difference vs. concentration) without averageing, and include zeros
slope, intercept = np.polyfit(
    calibration_data["conc"], calibration_data["difference"], 1
)

calibration_data = calibration_data.assign(
    calculated_conc=lambda x: (x["difference"] - intercept) / slope
)


analyzed_data = analyzed_data.assign(
    calculated_conc=lambda x: (x["difference"] - intercept) / slope
)

analyzed_data.to_csv("lunatic/data/LEFT.csv", index=False)
