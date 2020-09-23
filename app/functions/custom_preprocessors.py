import logging
import os
import pandas as pd
import re
import typer
from helpers.helpers import GlobalSettings


class CustomPreProcessors:
    """
    Custom pre-processing for selected input files.
    It MUST return dataframe object, ready to be processed by processing_functions.
    """
    @staticmethod
    def run_custom(country_name: str, make: str, filename: str):
        """
        Select custom process based on country name and car manufacturer.
        """
        logging.info("File preprocessing triggered!")

        if country_name == "Ireland" and make == "Ford":
            logging.info(f"Running for {country_name} / {make}")
            return CustomPreProcessors.ireland_ford(filename)

        elif country_name == "Australia" and make == "Porsche":
            logging.info(f"Running for {country_name} / {make}")
            return CustomPreProcessors.australia_porsche(filename)

        else:
            message = "Custom preprocessing settings not found!"
            logging.error(message)
            typer.echo(message)
            raise typer.Exit()

    @staticmethod
    def ireland_ford(filename: str):
        ford_file = filename
        ford_fixed = "ford_ireland_tempfile"

        partno_list = []
        price_list = []

        with open(os.path.join(GlobalSettings.acquisiton_folder, filename), 'r') as infile, open(ford_fixed, 'w') as outfile:
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
    def australia_porsche(filename: str):
        porsche_file = filename
        porsche_fixed = "porsche_australia_tempfile"

        partno_list = []
        price_list = []

        with open(os.path.join(GlobalSettings.acquisiton_folder, filename), 'r') as infile, open(porsche_fixed, 'w') as outfile:
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

