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
        if self.part_number_duplicates == 1:
            duplicates_dataframe = self.initial_dataframe[self.initial_dataframe.duplicated([str_part_no], keep=False)]
            if self.prefer_higher_price == 1:
                idmin = duplicates_dataframe.price.idxmin()
                self.initial_dataframe = self.initial_dataframe.drop(idmin).reset_index()

            elif self.prefer_higher_price == 0:
                idmax = duplicates_dataframe.price.idxmax()
                self.initial_dataframe = self.initial_dataframe.drop(idmax).reset_index()

            else:
                pass
        else:
            pass

        return self.initial_dataframe

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
