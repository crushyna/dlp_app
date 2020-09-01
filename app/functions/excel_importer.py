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


class ExcelProcessingObject(LocalizationProcessingSettings):

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

    def drop_duplicates(self):
        if self.part_number_duplicates == 1:
            duplicates_dataframe = self.initial_dataframe[self.initial_dataframe.duplicated([str_part_no], keep=False)]
            if len(duplicates_dataframe) != 0:

                if self.prefer_higher_price == 1:
                    idmin = duplicates_dataframe.price.idxmin()
                    self.initial_dataframe = self.initial_dataframe.drop(idmin)

                elif self.prefer_higher_price == 0:
                    idmax = duplicates_dataframe.price.idxmax()
                    self.initial_dataframe = self.initial_dataframe.drop(idmax)

            else:
                pass
        else:
            pass

        return self.initial_dataframe

    def drop_zero_prices(self):
        if self.zero_prices == 1:
            self.initial_dataframe = self.initial_dataframe[self.initial_dataframe.price != 0]

        else:
            pass

        return self.initial_dataframe

    def drop_zero_prices_alternative_parts(self):
        pass

    def drop_alternative_equals_original(self):
        pass

    def drop_null_part_no(self):
        """
        This might not work as expected and will require some fixing, since column PART_NO might be a string.
        :return: initial_dataframe
        """
        if self.alternative_equals_original == 1:
            self.initial_dataframe = self.initial_dataframe[(self.initial_dataframe.part_no != '0') &
                                                            (self.initial_dataframe.part_no != '0.0') &
                                                            (self.initial_dataframe.part_no != 0)]
        else:
            pass

        return self.initial_dataframe

    @staticmethod
    def read_excel_file(filename: str, header, names, index_col, skiprows: int, columns_to_use, engine: str):
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
        dataframe.columns = [str_part_no, str_price]

        # change price strings to floats
        dataframe[str_price] = dataframe[str_price].str.replace(",", ".")
        dataframe[str_price] = pd.to_numeric(dataframe[str_price])

        # clear part_no column from floats (if occur)
        dataframe[str_part_no] = dataframe[str_part_no].astype(str)
        dataframe[str_part_no] = dataframe[str_part_no].str.replace(r'[.][0]$', '', regex=True)

        return dataframe

    def save_to_fwf_txt(self):
        # get current timestamp
        current_timestamp = datetime.now().strftime('%d%m%y')

        output_dataframe = self.initial_dataframe
        output_dataframe[str_price] = output_dataframe[str_price].round(2)  # round float values
        output_dataframe.loc[-1] = [f'PriceL{current_timestamp}', 9.99]  # add timestamp mark
        output_dataframe.index = output_dataframe.index + 1  # shift index
        output_dataframe.sort_index(inplace=True)  # sort index
        output_dataframe = output_dataframe[[str_part_no, str_price]]

        fmt = f"%-{self.partno_end}s%+{self.position_price_start}.2f"
        filename = f"{self.country_short}_{self.make}_{current_timestamp}.txt"

        np.savetxt(f'{filename}', output_dataframe, fmt=fmt, encoding='utf-8')

        # Replace strings in .txt file
        SaveTxtHelper.replace_string(filename, ".", ",")
        SaveTxtHelper.replace_string(filename, "+", "")

        return 0
