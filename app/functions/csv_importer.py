import logging

import pandas as pd
import os

from config.config_parser import LocalizationProcessingSettings
from functions.processing_functions import ProcessingFunctions
from helpers.helpers import GlobalSettings

str_part_no = GlobalSettings.str_part_no
str_price = GlobalSettings.str_price


class CSVProcessingObject(LocalizationProcessingSettings, ProcessingFunctions):

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
        logging.info(f"Reading CSV file: {filename}")
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
        logging.debug(f"{filename}: naming columns")
        dataframe.columns = [str_part_no, str_price]

        # change price strings to floats
        logging.debug(f"{filename}: changing price to floats")
        dataframe[str_price] = dataframe[str_price].str.replace(",", ".")
        dataframe[str_price] = pd.to_numeric(dataframe[str_price])

        return dataframe
