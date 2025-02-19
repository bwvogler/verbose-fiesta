"open the serum uv data"

from typing import BinaryIO, Union, Callable
from enum import Enum
from abc import ABC, abstractmethod
import re

from boxy.models import ParsedData, Plate, Well  # noqa
from boxy.base_parser import BaseParser
from boxy.utils import get_first_xlsx_worksheet

import pandas as pd


def unpack_annotations(
    df: pd.DataFrame, annotations_column: str = "annotations"
) -> pd.DataFrame:
    return pd.concat(
        [
            df.drop(columns=[annotations_column]),
            pd.json_normalize(df[annotations_column]),
        ],
        axis=1,
    )


class SynergyApplication(ABC):
    """
    The base class for all Lunatic applications.
    """

    def __init__(self, name: str, version: str | None = None):
        self.name = name
        self.version = version

    @abstractmethod
    def header_conversion_dictionary(self, header: list[str]) -> dict[str, str]:
        """
        Converts the header of a Lunatic application to a dictionary of the column names and their corresponding values.
        Args:
            header (list[str]): The header of the Lunatic application.
        Returns:
            dict[str, str]: A dictionary of the column names and their corresponding values.
        """
        pass


class KineticTimeseries(SynergyApplication):
    """
    The class for the raw absorbance application of the Lunatic instrument.
    """

    def __init__(self, version=None):
        super().__init__("Raw Absorbance", version)

    def header_conversion_dictionary(self, header: list[str]) -> dict[str, str]:
        """
        Provides a dictionary for changing the column names of the raw absorbance application to just wavelength values.
        Args:
            header (list[str]): The header of the raw absorbance application.
        Returns:
            dict[str, str]: A dictionary of the column names and their corresponding values.
        """
        return dict(
            (column, column.split()[0][1:])
            for column in header
            if re.match(r"A\d+ \(10mm\)", column)
        )


class SynergyApplications(Enum):
    """
    Enum class for the different applications of the Lunatic instrument.
    Attributes
    ----------
    RAW_ABSORBANCE : str
        The raw absorbance application.
    """

    RAW_ABSORBANCE = KineticTimeseries


class ExcelParser(BaseParser):
    "All the Excel stuff"
    _well_column: str | None = None
    _well_string_to_row: Callable[[str], int] = lambda x: ord(x[0]) - 65
    _well_string_to_col: Callable[[str], int] = lambda x: int(x[1:]) - 1

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls._well_column is None:
            raise TypeError(
                f"Class variable 'well_column' must be set in {cls.__name__}"
            )

        if not isinstance(cls._well_string_to_row, staticmethod):
            cls._well_string_to_row = staticmethod(cls._well_string_to_row)

        if not isinstance(cls._well_string_to_col, staticmethod):
            cls._well_string_to_col = staticmethod(cls._well_string_to_col)

    @staticmethod
    def find_row_starting_with(sheet, value):
        """
        Finds the first row in the given sheet that starts with the specified value.
        Args:
            sheet (openpyxl.worksheet.worksheet.Worksheet): The worksheet to search through.
            value (str): The value to search for in the first cell of each row.
        Returns:
            int: The row number of the first row that starts with the specified value.
        Raises:
            StopIteration: If no row starts with the specified value.
        """

        return next(row[0].row for row in sheet.iter_rows() if row[0].value == value)

    @staticmethod
    def find_next_empty_row(sheet, start_row: int = 1):
        """
        Finds the next empty row in an Excel sheet starting from a specified row.

        Args:
            sheet: The Excel sheet object to search through.
            start_row (int, optional): The row number to start searching from. Defaults to 1.

        Returns:
            int: The row number of the next empty row.

        Raises:
            StopIteration: If no empty row is found.
        """
        return next(
            row[0].row
            for row in sheet.iter_rows(min_row=start_row)
            if all(cell.value is None for cell in row)
        )

    def _metadata_from_cell_range(self, sheet, start_row, end_row, start_col, end_col):
        """
        Extracts metadata from a range of cells in an Excel sheet.

        Args:
            sheet: The Excel sheet object to extract metadata from.
            start_row (int): The starting row number of the cell range.
            end_row (int): The ending row number of the cell range.
            start_col (int): The starting column number of the cell range.
            end_col (int): The ending column number of the cell range.

        Returns:
            dict: A dictionary containing the extracted metadata.
        """
        metadata = {}
        for row in sheet.iter_rows(
            min_row=start_row, max_row=end_row, min_col=start_col, max_col=end_col
        ):
            for cell in row:
                if cell.value is not None:
                    metadata[cell.value] = cell.offset(column=1).value
                    # advance to the next row
                    break
        return metadata

    def _well_df_from_cell_range(
        self,
        sheet,
        start_row,
        end_row,
        start_col,
        headers: list[str] | None = None,
    ):
        """
        Extracts well data from a range of cells in an Excel sheet.

        Args:
            sheet: The Excel sheet object to extract well data from.
            start_row (int): The starting row number of the cell range.
            end_row (int): The ending row number of the cell range.
            start_col (int): The starting column number of the cell range.
            end_col (int): The ending column number of the cell range.

        Returns:
            pd.DataFrame: A DataFrame containing the extracted well data.
        """
        if headers is None:
            headers = [cell.value for cell in sheet[start_row]]
        well_df = pd.DataFrame(
            sheet.iter_rows(
                min_row=start_row + 1,
                max_row=end_row,
                min_col=start_col,
                max_col=start_col + len(headers),
                values_only=True,
            ),
            columns=headers,
        )
        if "row" not in well_df.columns:
            well_df["row"] = None
        well_df.loc[:, "row"] = well_df[self._well_column].apply(
            self._well_string_to_row
        )
        if "col" not in well_df.columns:
            well_df["col"] = None
        well_df.loc[:, "col"] = well_df[self._well_column].apply(
            self._well_string_to_col
        )
        return well_df


class SynergyParser(ExcelParser):
    """
    LunaticParser is a parser class that extends the BaseParser to parse data from an Excel file.
    Methods
    -------
    parse(file: Union[str, BinaryIO]) -> ParsedData
        Parses the given Excel file and extracts metadata and sample data.
    parse(file: Union[str, BinaryIO]) -> ParsedData
        Parameters
        ----------
        file : Union[str, BinaryIO]
            The path to the Excel file or a file-like object containing the Excel data.
        Returns
        -------
        ParsedData
            An object containing the extracted metadata and sample data.
        Raises
        ------
        ValueError
            If there is an issue with reading the Excel file or finding the required data.
    """

    _well_column = "Plate Position"

    def parse(self, file: Union[str, BinaryIO]) -> ParsedData:
        # file = "uv/data/UV serum.xlsx"
        try:
            sheet = get_first_xlsx_worksheet(file)
        except ValueError as e:
            raise ValueError(e) from e
        # split the sheet into tables separated by empty rows
        section_starts = [
            (row[0].row + 3, row[0].offset(row=1).value)
            for row in sheet.iter_rows()
            if all(cell.value is None for cell in row)
            and all(cell.offset(row=2).value is None for cell in row)
            and row[0].offset(row=1).value is not None
        ]
        metadata = self._metadata_from_cell_range(
            sheet, 1, section_starts[1][0] - 2, 0, 2
        )
        tables = {
            str(table_name): pd.DataFrame(
                sheet.iter_rows(
                    start_row,
                    (
                        (section_starts[i + 1][0] - 4)
                        if i + 1 < len(section_starts)
                        else sheet.max_row
                    ),
                    2,
                    values_only=True,
                )
            )
            .dropna(how="all")
            .dropna(how="all", axis=1)
            .set_index(0)
            for i, (start_row, table_name) in enumerate(section_starts)
            if table_name != "Software Version"
        }
        # TODO: ensure that the tables are oriented with wells as rows
        table_indices = [
            (table_name, table.index)
            for table_name, table in tables.items()
            if any(well_name in table.index for well_name in ["A1", "A01"])
        ]
        well_location = "A1"
        kinetics = {
            table_name: tables[table_name]
            .loc[[table_index[0], well_location], :]
            .values
            for table_name, table_index in table_indices
        }

        list(tables.items())[-5]
        plates = [
            Plate(
                id=plate,
                wells=[
                    Well(
                        well_location=well["Plate Position"],
                        row=well["row"],
                        column=well["col"],
                        sample=well["Sample name"],
                        annotations={
                            # return a list of tuples with the (first row value, row with matching )
                            table_name: list(
                                zip(
                                    table.columns,
                                    row,
                                )
                            )
                        },
                    )
                    for _, well in plate_wells.iterrows()
                ],
            )
            for plate, plate_wells in plate_df.groupby("Plate ID")
        ]
        return ParsedData(
            metadata=metadata,
            plates=plates,
        )
