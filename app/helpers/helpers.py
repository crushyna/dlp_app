import configparser
import logging
import re
import sys
from dataclasses import dataclass
import os
import sqlite3
import pandas as pd
import typer
from pandas import DataFrame, Series
import operator


@dataclass
class GlobalSettings:
    config = configparser.ConfigParser()
    config.read('app/config/global_settings.ini')

    # TODO: delete str_* as they shouldn't be used
    acquisiton_folder = config['GLOBAL_APP_SETTINGS']['acquisiton_folder']
    localization_folder = config['GLOBAL_APP_SETTINGS']['localization_folder']
    output_folder = config['GLOBAL_APP_SETTINGS']['output_folder']
    str_part_no = config['GLOBAL_APP_SETTINGS']['str_part_no']
    str_part_ss = config['GLOBAL_APP_SETTINGS']['str_part_ss']
    str_price = config['GLOBAL_APP_SETTINGS']['str_price']
    return_console_messages = int(config['GLOBAL_APP_SETTINGS']['return_console_messages'])
    use_logs = int(config['GLOBAL_APP_SETTINGS']['use_logs'])
    logging_level = int(config['GLOBAL_APP_SETTINGS']['logging_level'])


class MainProgramHelper:

    @staticmethod
    def check_if_files_exist(filename: str, settings_file: str):
        if not os.path.isfile(os.path.join(GlobalSettings.acquisiton_folder, filename)):
            return f"File {filename} does not exist!"

        elif not os.path.isfile(os.path.join(GlobalSettings.localization_folder, settings_file)):
            return f"Settings file {settings_file} does not exist!"

        else:
            return True


class SaveTxtHelper:

    @staticmethod
    def set_file_formatting(alternative_parts: int,
                            force_price_as_string: int,
                            dataframe: object,
                            columns_output_names: list,
                            column1_start: int,
                            column1_length: int,
                            column2_start: int,
                            column2_length: int,
                            column3_start: int,
                            column3_length: int,
                            decimal_places: int,
                            alternative_float_column: int):
        try:
            if alternative_parts == 1:
                logging.debug("Setting file formatting for alternative_parts == 1")
                if force_price_as_string == 1:
                    logging.debug("Setting file formatting where prices are strings")
                    output_dataframe = dataframe[
                        list(columns_output_names)]
                    fmt = f"%-{column1_length + (column2_start - column1_length) - column1_start}s" \
                          f"%-{column2_length + (column3_start - column2_length) - column2_start}s" \
                          f"%{column3_length}s"

                else:
                    logging.debug("Setting file formatting where prices are floats")
                    output_dataframe = dataframe[
                        list(columns_output_names)]
                    if alternative_float_column != 1:
                        fmt = f"%-{column1_length + (column2_start - column1_length) - column1_start}s" \
                              f"%-{column2_length + (column3_start - column2_length) - column2_start}s" \
                              f"%{column3_length}.{decimal_places}f"

                        # TODO: this might need some fixing!
                    else:
                        fmt = f"%-{column1_length + (column2_start - column1_length) - column1_start}s" \
                              f"%-{column2_length + (column3_start - column2_length) - column2_start}s" \
                              f"%-{column3_length}.{decimal_places}f"

            else:
                logging.debug("Setting file formatting for alternative_parts == 0")
                if force_price_as_string == 1:
                    logging.debug("Setting file formatting where prices are strings")
                    output_dataframe = dataframe[
                        list(columns_output_names)]
                    fmt = f"%-{column1_length + (column2_start - column1_length) - column1_start}s" \
                          f"%-{column2_length}s"

                else:
                    logging.debug("Setting file formatting where prices are floats")
                    output_dataframe = dataframe[
                        list(columns_output_names)]
                    fmt = f"%-{column1_length + (column2_start - column1_length) - column1_start}s" \
                          f"%-{column2_length}.{decimal_places}f"

            return output_dataframe, fmt

        except Exception as er:
            logging.warning(er)
            typer.echo(er)
            sys.exit()

    @staticmethod
    def replace_string(filename: str, string: str, replacement: str):
        with open(filename, 'r', encoding='utf8') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(string, replacement)

        # Write the file out again
        with open(filename, 'w', encoding='utf8') as file:
            file.write(filedata)

        return filename


class DataframeHelpers:
    loop_query = """SELECT dataframe.part_no, dataframe.ss, dataframe.price FROM dataframe INNER JOIN dataframe AS 
                dataframe_1 ON (dataframe.ss = dataframe_1.part_no) AND (dataframe.part_no = dataframe_1.ss)"""

    missing_ss_query = """SELECT dataframe.ss, dataframe.price FROM dataframe WHERE dataframe.ss NOT IN (SELECT 
    dataframe.part_no FROM dataframe) AND dataframe.ss != ''"""

    @staticmethod
    def clear_loops(result_df: DataFrame, loop_prefer_higher_price: int):

        # TODO: this may require some cleaning and logging implementation
        fixed_dataframe = pd.DataFrame(columns=result_df.columns)
        exclusion_dataframe = pd.DataFrame(columns=result_df.columns)
        for each_index, each_row in result_df.iterrows():
            searched_row = (each_row[0], each_row[1])
            searched_row_price = each_row[2]
            reversed_row = searched_row[::-1]
            logging.debug(f"Searched row: {searched_row}")
            logging.debug(f"Searcher row price: {searched_row_price}")
            logging.debug(f"Reversed row: {reversed_row}")
            for each_index_1, each_row_1 in result_df.iterrows():
                temp_row = (each_row_1[0], each_row_1[1])
                temp_row_price = each_row_1[2]
                if reversed_row == temp_row:
                    logging.debug(f"Row found! Temp row: {temp_row}")
                    comparison_operator = operator.le if loop_prefer_higher_price == 1 else operator.ge
                    if comparison_operator(searched_row_price, temp_row_price):
                        logging.debug("Searched row price higher!")
                        fixed_dataframe.loc[-1] = [searched_row[0], searched_row[1], searched_row_price]
                        fixed_dataframe.index = fixed_dataframe.index + 1
                        fixed_dataframe = fixed_dataframe.sort_index()
                    else:
                        logging.debug("Searched row price lower!")
                        exclusion_dataframe.loc[-1] = [temp_row[0], temp_row[1], temp_row_price]
                        exclusion_dataframe.index = exclusion_dataframe.index + 1
                        exclusion_dataframe = exclusion_dataframe.sort_index()

        logging.debug(f"Excluded values: {exclusion_dataframe}")
        return exclusion_dataframe, fixed_dataframe

    @staticmethod
    def check_if_series_contain_special_chars(prices: Series):
        string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:+-]')
        for each_element in prices:
            if string_check.search(each_element) is None:
                pass
            else:
                return True
