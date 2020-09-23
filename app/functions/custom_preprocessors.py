import os
import pandas as pd
import re
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
        if country_name == "Ireland" and make == "Ford":
            return CustomPreProcessors.ireland_ford(filename)

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
                price_list.append(each_line[46:53])

        price_list = [x if x != '' else '0.00' for x in price_list]
        price_list = [x.strip() if x != '' else '0.00' for x in price_list]
        price_list = [0.00 if x == '' else x for x in price_list]

        partno_series = pd.Series(partno_list).astype(str)
        price_series = pd.Series(price_list).astype(float)

        dataframe = pd.DataFrame({"part_no": partno_series, "price": price_series})
        os.remove(ford_fixed)

        return dataframe
