from datetime import datetime
import numpy as np
import pandas as pd
from helpers.helpers import GlobalSettings, SaveTxtHelper, DataframeHelpers
import logging
import os


class ProcessingFunctions:
    initial_dataframe: object

    # TODO: deleting symbols like ,.[]\-= from part number

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

    def drop_loops(self):
        # TODO: works! but clean it!
        """
        iteritems and iterrows is too slow. Local temporary database is required.
        """
        if self.clear_loops == 1:
            logging.debug("Dropping loops")
            import sqlite3
            database_name = f"{self.country_short}_{self.make}_db"
            cnx = sqlite3.connect(database_name)
            df = self.initial_dataframe[self.initial_dataframe.ss != '']
            df.to_sql(name='dataframe', con=cnx)
            # cursor = cnx.cursor()

            result_df = pd.read_sql(DataframeHelpers.loop_query, con=cnx)
            exclusion_dataframe = DataframeHelpers.clear_loops(result_df, self.loop_prefer_higher_price)

            self.initial_dataframe = pd.concat([self.initial_dataframe, exclusion_dataframe]).drop_duplicates(keep=False)
            self.initial_dataframe.sort_index(inplace=True)

            cnx.close()
            os.remove(database_name)

            return self.initial_dataframe

        else:
            pass

    def drop_zero_prices(self):
        if self.zero_prices == 1:
            logging.debug("Dropping zero prices")
            self.initial_dataframe = self.initial_dataframe[self.initial_dataframe.price != 0]

        else:
            pass

        return self.initial_dataframe

    def create_prices_for_missing_ss(self):
        # TODO: continue here!
        pass

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
        """
        Drops NA values across whole dataset.
        :return:
        """
        if self.na_values == 1:
            logging.debug("Dropping NA values")
            self.initial_dataframe = self.initial_dataframe.dropna()

        else:
            pass

        return self.initial_dataframe

    def vat_setter(self):
        if self.vat_setting in (1, 2):
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

        # round float values
        output_dataframe = self.initial_dataframe
        output_dataframe[GlobalSettings.str_price] = output_dataframe[GlobalSettings.str_price].round(self.decimal_places)

        # add timestamp mark
        if self.alternative_parts == 1:
            output_dataframe.loc[-1] = [f'$${current_timestamp}', 9.99, '']  # add timestamp mark
        else:
            output_dataframe.loc[-1] = [f'PriceL{current_timestamp}', 9.99]  # add timestamp mark

        output_dataframe.index = output_dataframe.index + 1  # shift index
        output_dataframe.sort_index(inplace=True)  # sort index

        output_dataframe = output_dataframe[[GlobalSettings.str_part_no, GlobalSettings.str_part_ss, GlobalSettings.str_price]]

        if self.alternative_parts == 1:
            output_dataframe = output_dataframe[
                [GlobalSettings.str_part_no, GlobalSettings.str_part_ss, GlobalSettings.str_price]]
            fmt = f"%-{self.alternative_part_start - self.partno_start}s" \
                  f"%-{self.price_start - self.alternative_part_start}s" \
                  f"%{self.price_length}.{self.decimal_places}f"

        else:
            output_dataframe = output_dataframe[
                [GlobalSettings.str_part_no, GlobalSettings.str_part_ss, GlobalSettings.str_price]]
            fmt = f"%-{self.partno_start + self.partno_length}s%{self.price_start - self.price_length}.{self.decimal_places}f"

        filename = f"{self.country_short}_{self.make}_{current_timestamp}.txt"

        np.savetxt(fname=(os.path.join('app/output/', filename)), X=output_dataframe, fmt=fmt, encoding='utf-8')

        # Replace strings in .txt file
        logging.debug("Adding price list title")
        SaveTxtHelper.replace_string(os.path.join('app/output/', filename), f'$${current_timestamp}    ', f'PriceL{current_timestamp}')
        logging.debug("Replacing decimal separator")
        SaveTxtHelper.replace_string(os.path.join('app/output/', filename), ".", ",")

        logging.info("File saved successfully!")
        return 1
