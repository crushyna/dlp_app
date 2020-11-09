import logging
import os

from helpers.helpers import SaveTxtHelper, GlobalSettings


class PostProcessingFunctions:
    initial_dataframe: object

    # TODO: complete this
    # Replace strings in .txt file
    def post_update_timestamp_mark(self):
        if self.add_timestamp_mark:
            logging.debug("Adding price list title")
            SaveTxtHelper.replace_string(os.path.join(GlobalSettings.output_folder, self.output_filename),
                                         f'$$$$$${self.current_timestamp}',
                                         f'PriceL{self.current_timestamp}')

    def post_set_comma_decimal_sep(self):
        if self.set_comma_decimal_sep == 1:
            logging.debug("Replacing decimal separator")
            SaveTxtHelper.replace_string(os.path.join(GlobalSettings.output_folder, self.output_filename), ".", ",")

    def post_alternative_float_column(self):
        if self.alternative_float_column != 0:
            logging.debug("Replacing '+' with empty character")
            SaveTxtHelper.replace_string(os.path.join(GlobalSettings.output_folder, self.output_filename), "+", " ")

    def save_raw(self):
        pass
