import logging

import pandas as pd
import os

from config.config_parser import LocalizationProcessingSettings
from functions.processing_functions import ProcessingFunctions
from helpers.helpers import GlobalSettings


class CSVProcessingObject(LocalizationProcessingSettings, ProcessingFunctions):

    def __init__(self, filename: str, settings_file: str, engine=None):
        super().__init__(settings_file)
        self.filename = filename
        self.settings_file = settings_file
        self.engine = None if engine is None else engine

        self.initial_dataframe = self.read_csv_file()

    def read_csv_file(self):
        logging.info(f"Reading CSV file: {self.filename}")
        dataframe = pd.read_csv(os.path.join(GlobalSettings.acquisiton_folder, self.filename),
                                header=None if self.header is None else self.header,
                                names=None if self.names is None else self.names,
                                delimiter=None if self.delimiter is None else self.delimiter,
                                index_col=None if self.index_col is None else self.index_col,
                                usecols=tuple(self.columns_to_use),
                                skiprows=self.skiprows,
                                dtype=str,
                                engine=self.engine,
                                keep_default_na=False)

        # name columns properly
        logging.debug(f"{self.filename}: naming columns")
        dataframe.columns = self.columns_output_names

        # change price strings to floats
        logging.debug(f"{self.filename}: changing price to floats")
        dataframe.price = dataframe.price.str.replace(",", ".")
        dataframe.price = pd.to_numeric(dataframe.price)

        return dataframe
