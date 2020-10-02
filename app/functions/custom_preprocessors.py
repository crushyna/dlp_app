import logging
import os
import pandas as pd
import re
import typer
from datetime import datetime
from config.config_parser import LocalizationProcessingSettings
from helpers.helpers import GlobalSettings


class CustomPreProcessors:
    """
    Custom pre-processing for selected input files.
    It MUST return dataframe object, ready to be processed by processing_functions
    OR save file directly (when save_raw = 1).
    """

    @staticmethod
    def run_custom(country_name: str, make: str, filename: str, country_short: str):
        """
        Select custom process based on country name and car manufacturer.
        """
        logging.info("File pre-processing triggered!")
        logging.info(f"Running pre-processing for {country_name} / {make}")
        if country_name == "Ireland" and make == "Ford":
            return CustomPreProcessors.ireland_ford(filename)

        elif country_name == "Ireland" and make == "BMW":
            return CustomPreProcessors.ireland_bmw(filename, country_short, make)

        elif country_name == "Ireland" and make == "Fiat":
            return CustomPreProcessors.ireland_fiat(filename)

        elif country_name == "Australia" and make == "Porsche":
            return CustomPreProcessors.australia_porsche(filename)

        elif country_name == "Australia" and make == "Toyota":
            return CustomPreProcessors.australia_toyota(filename)

        elif country_name == "Australia" and make == "KIA":
            return CustomPreProcessors.australia_kia(filename)

        else:
            message = "Custom pre-processing settings not found!"
            logging.error(message)
            typer.echo(message)
            raise typer.Exit()

    @staticmethod
    def ireland_ford(filename: str):
        ford_file = filename
        ford_fixed = "ford_ireland_tempfile"

        partno_list = []
        price_list = []

        with open(os.path.join(GlobalSettings.acquisiton_folder, ford_file), 'r') as infile, open(ford_fixed, 'w') as outfile:
            content = infile.read()
            content_new = re.sub("P.N.E.", "  0.00", content, 0, re.DOTALL)
            outfile.write(content_new)
        with open(ford_fixed, 'r') as infile:
            for each_line in infile:
                partno_list.append(each_line[10:17])
                price_list.append(each_line[44:53])

        price_list = [x if x != '' else '0.00' for x in price_list]
        price_list = [x.strip() if x != '' else '0.00' for x in price_list]
        price_list = [0.00 if x == '' else x for x in price_list]

        partno_series = pd.Series(partno_list).astype(str)
        price_series = pd.Series(price_list).astype(float)

        dataframe = pd.DataFrame({"part_no": partno_series, "price": price_series})
        os.remove(ford_fixed)

        return dataframe

    @staticmethod
    def ireland_bmw(filename: str, country_short: str, make: str):
        bmw_file = filename
        current_timestamp = datetime.now().strftime('%d%m%y')
        output_filename = f"{country_short}_{make}_{current_timestamp}.txt"

        with open(os.path.join(GlobalSettings.acquisiton_folder, bmw_file), 'r') as infile, \
                open(os.path.join(GlobalSettings.output_folder, output_filename), 'w') as outfile:
            content = infile.read()
            content_new = re.sub("(.{60})", "\\1\n", content, 0, re.DOTALL)
            outfile.write(content_new)

    @staticmethod
    def ireland_fiat(filename: str):
        fiat_file = filename

        partno_list = []
        ss_list = []
        price_list = []

        with open(os.path.join(GlobalSettings.acquisiton_folder, fiat_file), 'r') as infile:
            for each_line in infile:
                partno_list.append(each_line[0:13])
                price_list.append(each_line[19:24] + '.' + each_line[24:26])
                ss_list.append(each_line[105:118])

        partno_series = pd.Series(partno_list).astype(str)
        ss_series = pd.Series(ss_list).astype(str)
        price_series = pd.Series(price_list).astype(float)

        dataframe = pd.DataFrame({"part_no": partno_series, "ss": ss_series, "price": price_series})

        return dataframe

    @staticmethod
    def australia_porsche(filename: str):
        porsche_file = filename

        porsche_fixed = "porsche_australia_tempfile"
        partno_list = []
        price_list = []

        with open(os.path.join(GlobalSettings.acquisiton_folder, porsche_file), 'r') as infile, open(porsche_fixed, 'w') as outfile:
            content = infile.read()
            content_new = re.sub("(.{500})", "\\1\n", content, 0, re.DOTALL)
            outfile.write(content_new)

        with open(porsche_fixed, 'r') as infile:
            for each_line in infile:
                partno_list.append(each_line[:14])
                price_list.append(each_line[117:125])

        partno_series = pd.Series(partno_list).astype(str)
        price_series = pd.Series(price_list).astype(str)

        dataframe = pd.DataFrame({"part_no": partno_series, "price": price_series})
        os.remove(porsche_fixed)

        return dataframe

    @staticmethod
    def australia_toyota(filename: str):
        toyota_file = filename

        partno_list = []
        ss_list = []
        price_list = []

        with open(os.path.join(GlobalSettings.acquisiton_folder, toyota_file), 'r') as infile:
            for each_line in infile:
                partno_list.append(each_line[8:20])
                ss_list.append('' if each_line[362:372].isspace() else f"{each_line[362:372]}     01")
                try:
                    price_list.append(re.search(r"([+].{13})", each_line[73:397])[0])
                except TypeError:
                    pass

        partno_series = pd.Series(partno_list).astype(str)
        ss_series = pd.Series(ss_list).astype(str)
        price_series = pd.Series(price_list).astype(str)

        dataframe = pd.DataFrame({"part_no": partno_series, "ss": ss_series, "price": price_series})
        dataframe = dataframe.iloc[2:][:-1].reset_index(drop=True)

        return dataframe

    @staticmethod
    def australia_kia(filename):
        kia_file = filename

        partno_list = []
        # ss_list = []
        price_list = []

        with open(os.path.join(GlobalSettings.acquisiton_folder, kia_file), 'r') as infile:
            for _ in range(1):
                next(infile)
            for each_line in infile:
                partno_list.append(each_line[1:23])
                price_list.append(each_line[53:61])
                # ss_list.append(each_line[63:64])

        partno_series = pd.Series(partno_list).astype(str)
        price_series = pd.Series(price_list).astype(float)
        # ss_series = pd.Series(ss_list).astype(str)

        # dataframe = pd.DataFrame({"part_no": partno_series, "price": price_series, "ss": ss_series})
        dataframe = pd.DataFrame({"part_no": partno_series, "price": price_series})

        # dataframe.ss = dataframe.ss.astype(str).str.strip()
        dataframe.part_no = dataframe.part_no.str.strip()

        return dataframe
