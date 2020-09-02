from datetime import datetime
import numpy as np
from helpers.helpers import GlobalSettings, SaveTxtHelper
import logging


class ProcessingFunctions:
    initial_dataframe: object

    def drop_duplicates(self):
        if self.part_number_duplicates == 1:
            logging.debug("Dropping duplicates")
            duplicates_dataframe = self.initial_dataframe[
                self.initial_dataframe.duplicated([GlobalSettings.str_part_no], keep=False)]
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
            logging.debug("Dropping zero prices")
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
            logging.debug("Dropping null part_no")
            self.initial_dataframe = self.initial_dataframe[(self.initial_dataframe.part_no != '0') &
                                                            (self.initial_dataframe.part_no != '0.0') &
                                                            (self.initial_dataframe.part_no != 0)]
        else:
            pass

        return self.initial_dataframe

    def drop_na_values(self):
        if self.na_values == 1:
            logging.debug("Dropping NA values")
            self.initial_dataframe = self.initial_dataframe.dropna()

        else:
            pass

        return self.initial_dataframe

    def vat_setter(self):
        if self.vat_setting == 1 or 2:
            logging.debug("Calculating new prices (VAT)")
            if self.vat_setting == 1:
                self.initial_dataframe.price = self.initial_dataframe.price * (1 + (self.vat_value/100))

            elif self.vat_setting == 2:
                self.initial_dataframe.price = self.initial_dataframe.price * (1 - (self.vat_value/100))

            else:
                pass

        else:
            pass

        return self.initial_dataframe

    def save_to_fwf_txt(self):
        logging.debug(f"Saving dataframe to FWF text file")
        # get current timestamp
        current_timestamp = datetime.now().strftime('%d%m%y')

        output_dataframe = self.initial_dataframe
        output_dataframe[GlobalSettings.str_price] = output_dataframe[GlobalSettings.str_price].round(2)
        output_dataframe.loc[-1] = [f'PriceL{current_timestamp}', 9.99]  # add timestamp mark
        output_dataframe.index = output_dataframe.index + 1  # shift index
        output_dataframe.sort_index(inplace=True)  # sort index
        output_dataframe = output_dataframe[[GlobalSettings.str_part_no, GlobalSettings.str_price]]

        fmt = f"%-{self.partno_end}s%{self.position_price_start}.2f"
        fmt = f"%-{self.partno_end}s%{self.position_price_start}.{self.decimal_places}f"
        filename = f"{self.country_short}_{self.make}_{current_timestamp}.txt"

        np.savetxt(f'{filename}', output_dataframe, fmt=fmt, encoding='utf-8')

        # Replace strings in .txt file
        logging.debug(f"Replacing decimal separator")
        SaveTxtHelper.replace_string(filename, ".", ",")

        return 1
