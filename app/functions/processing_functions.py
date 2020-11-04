import sys
from datetime import datetime
import numpy as np
import pandas as pd
import typer

from helpers.helpers import GlobalSettings, SaveTxtHelper, DataframeHelpers
from pandas.io.sql import DatabaseError
import logging
import os


class ProcessingFunctions:
    initial_dataframe: object

    # TODO: deleting symbols like ,.[]\-= from part number

    current_timestamp: str = datetime.now().strftime('%d%m%y')

    def drop_duplicates(self) -> object:
        if self.part_number_duplicates == 1:
            logging.debug("Dropping duplicates")
            self.initial_dataframe.drop_duplicates(inplace=True)

            duplicates_dataframe = self.initial_dataframe[
                self.initial_dataframe.duplicated([GlobalSettings.str_part_no], keep=False)]
            if len(duplicates_dataframe) != 0:
                # remove all duplicates
                self.initial_dataframe = pd.concat([self.initial_dataframe, duplicates_dataframe]).drop_duplicates(
                    keep=False)

                if self.prefer_higher_price == 1:
                    # add proper one
                    values_to_add = duplicates_dataframe.sort_values('price').drop_duplicates(subset='part_no',
                                                                                              keep='last')
                    self.initial_dataframe = self.initial_dataframe.append(values_to_add, sort='false')

                    # save changes & reset index
                    self.initial_dataframe.reset_index(inplace=True, drop=True)

                elif self.prefer_higher_price == 0:
                    # add proper one
                    values_to_add = duplicates_dataframe.sort_values('price').drop_duplicates(subset='part_no',
                                                                                              keep='first')
                    self.initial_dataframe = self.initial_dataframe.append(values_to_add, sort='false')

                    # save changes & reset index
                    self.initial_dataframe.reset_index(inplace=True, drop=True)

            else:
                logging.warning("No duplicates found!")

        return self.initial_dataframe

    def drop_loops(self) -> object:
        """
        Function for dropping loops.
        For specific information about this function, look into DataframeHelpers.clear_loops() function.
        iteritems and iterrows is too slow. Local temporary database is required.
        """
        if self.clear_loops == 1:
            try:
                logging.debug("Dropping loops")
                import sqlite3
                database_name = f"{self.country_short}_{self.make}_loops_db"
                cnx = sqlite3.connect(os.path.join(GlobalSettings.temp_folder, database_name))
                df = self.initial_dataframe[self.initial_dataframe.ss != '']
                df.to_sql(name='dataframe', con=cnx)

                result_df = pd.read_sql(DataframeHelpers.loop_query, con=cnx)
                exclusion_dataframe, fixed_dataframe = DataframeHelpers.clear_loops(result_df,
                                                                                    self.loop_prefer_higher_price)

                self.initial_dataframe = pd.concat([self.initial_dataframe, exclusion_dataframe]).drop_duplicates(
                    keep=False)
                self.initial_dataframe.sort_index(inplace=True)

                cnx.close()
                os.remove(os.path.join(GlobalSettings.temp_folder, database_name))

            except AttributeError as er:
                message = "Loops cannot be identified since there is no SS column! Please check .ini file!"
                logging.critical(er)
                logging.error(message)
                typer.echo(message)
                raise typer.Exit()

        return self.initial_dataframe

    def drop_zero_prices(self) -> object:
        if self.zero_prices == 1:
            logging.debug("Dropping zero prices")
            self.initial_dataframe = self.initial_dataframe[self.initial_dataframe.price != 0]

        return self.initial_dataframe

    def create_prices_for_missing_ss(self) -> object:
        try:
            if self.add_prices_for_missing_ss == 1:
                logging.debug("Creating missing prices for SS")
                import sqlite3
                database_name = f"{self.country_short}_{self.make}_ssprices_db"
                cnx = sqlite3.connect(os.path.join(GlobalSettings.temp_folder, database_name))
                df = self.initial_dataframe.copy(deep=True)
                df.to_sql(name='dataframe', con=cnx, index=False)

                additions_dataframe = pd.read_sql(DataframeHelpers.missing_ss_query, con=cnx)
                additions_dataframe['ss_1'] = ''  # add temporary column
                additions_dataframe.columns = self.columns_input_names  # and change it's name :)

                self.initial_dataframe = self.initial_dataframe.append(additions_dataframe, sort='false')
                self.initial_dataframe.reset_index(inplace=True, drop=True)

                if self.force_price_as_string == 0:
                    self.initial_dataframe.price = pd.to_numeric(self.initial_dataframe.price)

                cnx.close()
                os.remove(os.path.join(GlobalSettings.temp_folder, database_name))

        except DatabaseError as er:
            message = "Prices for SS cannot be created since there is no SS column! Please check .ini file!"
            logging.critical(er)
            logging.error(message)
            typer.echo(message)
            sys.exit()

        return self.initial_dataframe

    def drop_zero_prices_alternative_parts(self):
        pass

    def drop_alternative_equals_original(self):
        pass

    def drop_null_part_no(self) -> object:
        """
        This might not work as expected and will require some fixing, since column PART_NO might be a string.
        :return: initial_dataframe
        """
        if self.null_part_number == 1:
            logging.debug("Dropping null part_no")
            self.initial_dataframe = self.initial_dataframe[(self.initial_dataframe.part_no != '0') &
                                                            (self.initial_dataframe.part_no != '0.0') &
                                                            (self.initial_dataframe.part_no != 0) &
                                                            (self.initial_dataframe.part_no != '') &
                                                            (self.initial_dataframe.part_no != ' ')]

        return self.initial_dataframe

    def drop_na_values(self) -> object:
        """
        Drops NA values across whole dataset.
        :return:
        """
        if self.na_values == 1:
            logging.debug("Dropping NA values")
            self.initial_dataframe = self.initial_dataframe.dropna(how='all')

        return self.initial_dataframe

    def drop_na_partno(self) -> object:
        # TODO: barely happens, but nice to have
        """
        Drop row when part_no is empty.
        :return: object
        """
        pass

    def vat_setter(self) -> object:
        if self.vat_setting in (1, 2):
            logging.debug("Calculating new prices (VAT)")
            if self.vat_setting == 1:
                self.initial_dataframe.price = self.initial_dataframe.price * (1 + (self.vat_value / 100))

            elif self.vat_setting == 2:
                self.initial_dataframe.price = self.initial_dataframe.price * (1 - (self.vat_value / 100))

        return self.initial_dataframe

    def save_to_fwf_txt(self) -> str:
        global update_timestamp_mark
        update_timestamp_mark = False
        logging.debug(f"Saving dataframe to FWF text file")
        output_dataframe = self.initial_dataframe

        try:
            if self.clear_characters == 1:
                logging.debug("Removing unwanted characters")
                output_dataframe = SaveTxtHelper.remove_unwanted_characters(output_dataframe, self.characters_to_remove)

            # TODO: add this for Land Rover and Jaguar. Maybe in pre-processing?
            '''
            logging.debug("Removing unwanted characters")
            output_dataframe.ss = output_dataframe.ss.str.replace("O", "")
            '''

            if self.force_price_as_string == 0:
                output_dataframe.price = output_dataframe.price.round(
                    self.decimal_places)
            else:
                logging.warning(f"Prices will be saved as strings (FORCED).")
                typer.echo(f"Prices will be saved as strings (FORCED).")

            # add timestamp mark
            if self.add_timestamp_mark == 1:
                update_timestamp_mark = True
                if self.alternative_parts == 1:
                    logging.debug("Setting timestamp for alternative_parts == 1")
                    output_dataframe.loc[-1] = [f'$$$$$${ProcessingFunctions.current_timestamp}', 9.99, '']  # add timestamp mark

                else:
                    logging.debug("Setting timestamp for alternative_parts == 0")
                    output_dataframe.loc[-1] = [f'$$$$$${ProcessingFunctions.current_timestamp}', 9.99]  # add timestamp mark

                output_dataframe.index = output_dataframe.index + 1  # shift index
                output_dataframe.sort_index(inplace=True)  # sort index

            # check formatting
            output_dataframe, fmt = SaveTxtHelper.set_file_formatting(self.alternative_parts, self.force_price_as_string,
                                                                      output_dataframe,
                                                                      self.columns_output_names, self.column1_start,
                                                                      self.column1_length,
                                                                      self.column2_start, self.column2_length,
                                                                      self.column3_start,
                                                                      self.column3_length, self.decimal_places,
                                                                      self.alternative_float_column)

            # clear whole dataframe from NAN's
            logging.debug("Clearing NaNs")
            output_dataframe = output_dataframe.fillna('')

            # set columns to strings (just in case they aren't)
            output_dataframe.part_no = output_dataframe.part_no.astype(str)
            if self.alternative_parts == 1:
                output_dataframe.ss = output_dataframe.ss.astype(str)

        except Exception as er:
            logging.critical(f"Critical error! {er}")
            typer.echo(f"Critical error! {er}")

        # set filename and save file
        filename = f"{self.country_short}_{self.make}_{ProcessingFunctions.current_timestamp}.txt"

        try:
            np.savetxt(fname=(os.path.join(GlobalSettings.output_folder, filename)), X=output_dataframe, fmt=fmt,
                       encoding='utf-8')

        # TODO: this makes nightmares with Australia FIAT / FAR
        except TypeError as er:
            logging.warning(f"Error while writing .txt file! {er}. Please check output file!")
            typer.echo(f"Error while writing .txt file! {er}. Please check output file!")

        # Replace strings in .txt file
        if update_timestamp_mark:
            logging.debug("Adding price list title")
            SaveTxtHelper.replace_string(os.path.join(GlobalSettings.output_folder, filename),
                                         f'$$$$$${ProcessingFunctions.current_timestamp}',
                                         f'PriceL{ProcessingFunctions.current_timestamp}')

        if self.set_comma_decimal_sep == 1:
            logging.debug("Replacing decimal separator")
            SaveTxtHelper.replace_string(os.path.join(GlobalSettings.output_folder, filename), ".", ",")

        if self.alternative_float_column != 0:
            logging.debug("Replacing '+' with empty character")
            SaveTxtHelper.replace_string(os.path.join(GlobalSettings.output_folder, filename), "+", " ")

        # finish process
        logging.info("File saved successfully!")

        return filename
