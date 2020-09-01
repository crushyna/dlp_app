from typing import Optional

import pandas as pd
import numpy as np
import os
import xlrd
from datetime import datetime
import pyxlsb

from config.config_parser import LocalizationProcessingSettings
from helpers.helpers import SaveTxtHelper, GlobalSettings

str_part_no = GlobalSettings.str_part_no
str_price = GlobalSettings.str_price


class CSVProcessingObject(LocalizationProcessingSettings):

    def __init__(self, filename: str, settings_file: str, engine=None):
        super().__init__(settings_file)
        self.filename = filename
        self.settings_file = settings_file
        self.engine = None if engine is None else engine

        self.initial_dataframe = self.read_csv_file(self.filename,
                                                    self.header,
                                                    self.names,
                                                    self.delimiter,
                                                    self.index_col,
                                                    self.skiprows,
                                                    self.columns_to_use,
                                                    self.engine)

    @staticmethod
    def read_csv_file(filename: str, header, names, delimiter, index_col, skiprows: int, columns_to_use, engine: str):
        dataframe = pd.read_csv(os.path.join(GlobalSettings.acquisiton_folder, filename),
                                header=None if header is None else header,
                                names=None if names is None else names,
                                delimiter=delimiter,
                                index_col=None if index_col is None else index_col,
                                usecols=tuple(columns_to_use),
                                skiprows=skiprows,
                                dtype=str,
                                engine=engine)

        # name columns properly
        dataframe.columns = [str_part_no, str_price]

        # change price strings to floats
        dataframe[str_price] = dataframe[str_price].str.replace(",", ".")
        dataframe[str_price] = pd.to_numeric(dataframe[str_price])

        # clear part_no column from floats (if occur)
        dataframe[str_part_no] = dataframe[str_part_no].astype(str)
        dataframe[str_part_no] = dataframe[str_part_no].str.replace(r'[.][0]$', '', regex=True)

        return dataframe
