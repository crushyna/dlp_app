import logging
import pandas as pd
import os
import typer
import xlrd
import pyxlsb
from pandas import DataFrame

from config.config_parser import LocalizationProcessingSettings
from functions.custom_preprocessors import CustomPreProcessors
from functions.post_processing import PostProcessingFunctions
from functions.processing_functions import ProcessingFunctions
from helpers.helpers import GlobalSettings


class ExcelProcessingObject(LocalizationProcessingSettings, ProcessingFunctions, PostProcessingFunctions):

    def __init__(self, filename: str, settings_file: str, engine: str):
        super().__init__(settings_file)
        self.filename = filename
        self.settings_file = settings_file
        self.engine = None if engine is None else engine

        self.initial_dataframe = CustomPreProcessors.run_custom(self.country_name,
                                                                self.make,
                                                                self.filename,
                                                                self.country_short,
                                                                self.column3_length) \
            if self.custom_settings == 1 else self.read_csv_file()

    def read_excel_file(self) -> DataFrame:
        try:
            logging.info(f"Reading Excel file: {self.filename}")
            dataframe = pd.read_excel(os.path.join(GlobalSettings.acquisiton_folder, self.filename),
                                      header=None if self.header is None else self.header,
                                      names=None if self.names is None else self.names,
                                      index_col=None if self.index_col is None else self.index_col,
                                      usecols=tuple(self.columns_to_use),
                                      convert_float=False,
                                      skiprows=self.skiprows,
                                      dtype=str,
                                      engine=self.engine)

            # name columns properly
            logging.debug(f"{self.filename}: naming columns")
            dataframe.columns = self.columns_input_names

            # change price strings to floats
            logging.debug(f"{self.filename}: changing price to floats")
            dataframe.price = dataframe.price.str.replace(",", ".")
            dataframe.price = pd.to_numeric(dataframe.price)

            # clear part_no column from floats (if occur)
            logging.debug(f"{self.filename}: clearing part_no column")
            dataframe.part_no = dataframe.part_no.astype(str)
            dataframe.part_no = dataframe.part_no.str.replace(r'[.][0]$', '', regex=True)

            return dataframe

        except Exception as er:
            message = "Error when reading Excel file!"
            logging.critical(er)
            logging.critical(message)
            typer.echo(message)
            raise typer.Exit()

