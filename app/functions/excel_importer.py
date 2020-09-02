import logging

import pandas as pd
import os
import xlrd
import pyxlsb

from config.config_parser import LocalizationProcessingSettings
from functions.processing_functions import ProcessingFunctions
from helpers.helpers import GlobalSettings

str_part_no = GlobalSettings.str_part_no
str_price = GlobalSettings.str_price


class ExcelProcessingObject(LocalizationProcessingSettings, ProcessingFunctions):

    def __init__(self, filename: str, settings_file: str, engine: str):
        super().__init__(settings_file)
        self.filename = filename
        self.settings_file = settings_file
        self.engine = None if engine is None else engine

        self.initial_dataframe = self.read_excel_file(self.filename,
                                                      self.header,
                                                      self.names,
                                                      self.index_col,
                                                      self.skiprows,
                                                      self.columns_to_use,
                                                      self.engine)

    @staticmethod
    def read_excel_file(filename: str, header, names, index_col, skiprows: int, columns_to_use, engine: str):
        logging.info(f"Reading Excel file: {filename}")
        dataframe = pd.read_excel(os.path.join(GlobalSettings.acquisiton_folder, filename),
                                  header=None if header is None else header,
                                  names=None if names is None else names,
                                  index_col=None if index_col is None else index_col,
                                  usecols=tuple(columns_to_use),
                                  convert_float=False,
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

        # clear part_no column from floats (if occur)
        logging.debug(f"{filename}: clearing part_no column")
        dataframe[str_part_no] = dataframe[str_part_no].astype(str)
        dataframe[str_part_no] = dataframe[str_part_no].str.replace(r'[.][0]$', '', regex=True)

        return dataframe

