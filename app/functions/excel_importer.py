import pandas as pd
import numpy as np
import os
import xlrd

from config.config_parser import LocalizationProcessingSettings


class ExcelProcessingObject(LocalizationProcessingSettings):

    def __init__(self, filename: str, settings_file: str):
        super().__init__(settings_file)
        self.filename = filename
        self.settings_file = settings_file

        self.initial_dataframe = self.read_excel_file(self.filename,
                                                      self.header,
                                                      self.names,
                                                      self.index_col,
                                                      self.skiprows)

    @staticmethod
    def read_excel_file(filename: str, header, names, index_col, skiprows: int):
        dataframe = pd.read_excel(os.path.join('app/acquisition/', filename),
                                  header=None if header == 'None' else header,
                                  names=None if names == 'None' else names,
                                  index_col=None if index_col == 'None' else index_col,
                                  usecols="A,C",
                                  convert_float=False,
                                  skiprows=skiprows)

        # name columns properly
        dataframe.columns = ['part_no', 'price']

        # change comma separators
        dataframe = dataframe.apply(lambda x: x.str.replace(',', '.'))

        # change price objects to floats
        dataframe['price'] = pd.to_numeric(dataframe['price'])

        # change type "object" to string
        dataframe['part_no'] = dataframe['part_no'].astype('str')

        return dataframe
