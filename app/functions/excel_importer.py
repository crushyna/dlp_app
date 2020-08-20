import pandas as pd
import numpy as np
import os
import xlrd

from config.config_parser import LocalizationProcessingSettings

str_part_no = "part_no"
str_price = "price"


class ExcelProcessingObject(LocalizationProcessingSettings):

    def __init__(self, filename: str, settings_file: str):
        super().__init__(settings_file)
        self.filename = filename
        self.settings_file = settings_file

        self.initial_dataframe = self.read_excel_file(self.filename,
                                                      self.header,
                                                      self.names,
                                                      self.index_col,
                                                      self.skiprows,
                                                      self.columns_to_use)

    def drop_duplicates(self):
        # self.initial_dataframe.drop_duplicates()
        # self.initial_dataframe = self.initial_dataframe.sort_values('part_no', ascending=False).drop_duplicates('part_no',keep='last').sort_index()
        # self.initial_dataframe = self.initial_dataframe.sort_values('price').drop_duplicates('part_no', keep='last')

        # duplicated_rows = self.initial_dataframe[self.initial_dataframe.duplicated()]
        # pd.concat(g for _, g in self.initial_dataframe.groupby(str_part_no) if len(g) > 1)

        duplicated_rows = self.initial_dataframe[self.initial_dataframe.duplicated([str_part_no], keep=False)]

        return duplicated_rows

    @staticmethod
    def read_excel_file(filename: str, header, names, index_col, skiprows: int, columns_to_use):
        dataframe = pd.read_excel(os.path.join('app/acquisition/', filename),
                                  header=None if header == 'None' else header,
                                  names=None if names == 'None' else names,
                                  index_col=None if index_col == 'None' else index_col,
                                  usecols=columns_to_use,
                                  convert_float=False,
                                  skiprows=skiprows,
                                  dtype=str)

        # name columns properly
        dataframe.columns = [str_part_no, str_price]

        # change comma separators
        dataframe = dataframe.apply(lambda x: x.str.replace(',', '.'))

        # change price objects to floats
        dataframe[str_price] = pd.to_numeric(dataframe[str_price])

        return dataframe
