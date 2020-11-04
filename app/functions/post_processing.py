import logging
import os

from functions.processing_functions import ProcessingFunctions
from helpers.helpers import SaveTxtHelper, GlobalSettings


class PostProcessingFunctions:
    initial_dataframe: object

    # TODO: complete this
    # Replace strings in .txt file
    def update_timestamp_mark(self):
        if self.update_timestamp_mark:
            logging.debug("Adding price list title")
            SaveTxtHelper.replace_string(os.path.join(GlobalSettings.output_folder, self.filename),
                                         f'$$$$$${self.current_timestamp}',
                                         f'PriceL{self.current_timestamp}')

    def set_comma_decimal_sep(self):
        if self.set_comma_decimal_sep == 1:
            logging.debug("Replacing decimal separator")
            SaveTxtHelper.replace_string(os.path.join(GlobalSettings.output_folder, self.filename), ".", ",")

    def alternative_float_column(self):
        if self.alternative_float_column != 0:
            logging.debug("Replacing '+' with empty character")
            SaveTxtHelper.replace_string(os.path.join(GlobalSettings.output_folder, self.filename), "+", " ")

    def save_raw(self):
        pass
