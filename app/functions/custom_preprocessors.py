import logging
import os
from typing import List

import pandas as pd
import re
import typer
from datetime import datetime

from pandas import DataFrame

from helpers.helpers import GlobalSettings


class CustomPreProcessors:
    """
    Custom pre-processing for selected input files.
    It MUST return dataframe object, ready to be processed by processing_functions
    OR save file directly (when save_raw = 1).
    """

    partno_list: List[str] = []
    ss_list: List[str] = []
    price_list: List[str or float] = []

    partno_series = pd.Series(dtype=str)
    ss_series = pd.Series(dtype=str)
    price_series = pd.Series(dtype=str)

    output_filename: str

    @staticmethod
    def run_custom(country_name: str, make: str, filename: str, country_short: str) -> DataFrame or str:
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

        elif country_name == "Australia" and make == "Tesla":
            return CustomPreProcessors.australia_tesla(filename)

        elif country_name == "Australia" and make == "TeslaSS":
            return CustomPreProcessors.australia_tesla_ss(filename, country_short, make)

        else:
            message = "Custom pre-processing settings not found!"
            logging.error(message)
            typer.echo(message)
            raise typer.Exit()

    @classmethod
    def ireland_ford(cls, filename) -> DataFrame:
        ford_file = filename
        ford_fixed = "ford_ireland_tempfile"

        with open(os.path.join(GlobalSettings.acquisiton_folder, ford_file), 'r') as infile, open(ford_fixed,
                                                                                                  'w') as outfile:
            content = infile.read()
            content_new = re.sub("P.N.E.", "  0.00", content, 0, re.DOTALL)
            outfile.write(content_new)
        with open(ford_fixed, 'r') as infile:
            for each_line in infile:
                cls.partno_list.append(each_line[10:17])
                cls.price_list.append(each_line[44:53])

        cls.price_list = [x if x != '' else '0.00' for x in cls.price_list]
        cls.price_list = [x.strip() if x != '' else '0.00' for x in cls.price_list]
        cls.price_list = [0.00 if x == '' else x for x in cls.price_list]

        cls.partno_series = pd.Series(cls.partno_list).astype(str)
        cls.price_series = pd.Series(cls.price_list).astype(float)

        dataframe = pd.DataFrame({"part_no": cls.partno_series, "price": cls.price_series})
        os.remove(ford_fixed)

        return dataframe

    @classmethod
    def ireland_bmw(cls, filename: str, country_short: str, make: str) -> str:
        bmw_file = filename
        current_timestamp = datetime.now().strftime('%d%m%y')
        cls.output_filename = f"{country_short}_{make}_{current_timestamp}.txt"

        with open(os.path.join(GlobalSettings.acquisiton_folder, bmw_file), 'r') as infile, \
                open(os.path.join(GlobalSettings.output_folder, cls.output_filename), 'w') as outfile:
            content = infile.read()
            content_new = re.sub("(.{60})", "\\1\n", content, 0, re.DOTALL)
            outfile.write(content_new)

        return cls.output_filename

    @classmethod
    def ireland_fiat(cls, filename: str) -> DataFrame:
        fiat_file = filename

        with open(os.path.join(GlobalSettings.acquisiton_folder, fiat_file), 'r') as infile:
            for each_line in infile:
                cls.partno_list.append(each_line[0:13])
                cls.price_list.append(each_line[19:24] + '.' + each_line[24:26])
                cls.ss_list.append(each_line[105:118])

        cls.partno_series = pd.Series(cls.partno_list).astype(str)
        cls.ss_series = pd.Series(cls.ss_list).astype(str)
        cls.price_series = pd.Series(cls.price_list).astype(float)

        dataframe = pd.DataFrame({"part_no": cls.partno_series, "ss": cls.ss_series, "price": cls.price_series})

        return dataframe

    @classmethod
    def australia_porsche(cls, filename: str) -> DataFrame:
        porsche_file = filename
        porsche_fixed = "porsche_australia_tempfile"

        with open(os.path.join(GlobalSettings.acquisiton_folder, porsche_file), 'r') as infile, open(porsche_fixed,
                                                                                                     'w') as outfile:
            content = infile.read()
            content_new = re.sub("(.{500})", "\\1\n", content, 0, re.DOTALL)
            outfile.write(content_new)

        with open(porsche_fixed, 'r') as infile:
            for each_line in infile:
                cls.partno_list.append(each_line[:14])
                cls.price_list.append(each_line[117:125])

        cls.partno_series = pd.Series(cls.partno_list).astype(str)
        cls.price_series = pd.Series(cls.price_list).astype(str)

        dataframe = pd.DataFrame({"part_no": cls.partno_series, "price": cls.price_series})
        os.remove(porsche_fixed)

        return dataframe

    @classmethod
    def australia_toyota(cls, filename: str) -> DataFrame:
        toyota_file = filename

        with open(os.path.join(GlobalSettings.acquisiton_folder, toyota_file), 'r') as infile:
            for each_line in infile:
                cls.partno_list.append(each_line[8:20])
                cls.ss_list.append('' if each_line[362:372].isspace() else f"{each_line[362:372]}     01")
                try:
                    cls.price_list.append(re.search(r"([+].{13})", each_line[73:397])[0])
                except TypeError:
                    pass

        cls.partno_series = pd.Series(cls.partno_list).astype(str)
        cls.ss_series = pd.Series(cls.ss_list).astype(str)
        cls.price_series = pd.Series(cls.price_list).astype(str)

        dataframe = pd.DataFrame({"part_no": cls.partno_series, "ss": cls.ss_series, "price": cls.price_series})
        dataframe = dataframe.iloc[2:][:-1].reset_index(drop=True)

        return dataframe

    @classmethod
    def australia_kia(cls, filename: str) -> DataFrame:
        kia_file = filename

        with open(os.path.join(GlobalSettings.acquisiton_folder, kia_file), 'r') as infile:
            for _ in range(1):
                next(infile)
            for each_line in infile:
                cls.partno_list.append(each_line[1:23])
                cls.price_list.append(each_line[53:61])
                # ss_list.append(each_line[63:64])

        cls.partno_series = pd.Series(cls.partno_list).astype(str)
        cls.price_series = pd.Series(cls.price_list).astype(float)
        # ss_series = pd.Series(ss_list).astype(str)

        # dataframe = pd.DataFrame({"part_no": partno_series, "price": price_series, "ss": ss_series})
        dataframe = pd.DataFrame({"part_no": cls.partno_series, "price": cls.price_series})

        # dataframe.ss = dataframe.ss.astype(str).str.strip()
        dataframe.part_no = dataframe.part_no.str.strip()

        return dataframe

    @classmethod
    def australia_tesla(cls, filename: str) -> DataFrame:
        dataframe = pd.read_csv(os.path.join(GlobalSettings.acquisiton_folder, filename), names=['part_no', 'price', 'currency', 'ss'], header=0)
        dataframe = dataframe[['part_no', 'ss', 'price']][dataframe.ss == 'AU']

        dataframe.part_no = dataframe.part_no.str.replace("-", "")
        dataframe.part_no = dataframe.part_no.astype(str)
        dataframe.ss = dataframe.ss.astype(str)
        dataframe.price = dataframe.price.astype(float)

        return dataframe

    @classmethod
    def australia_tesla_ss(cls, filename: str, country_short: str, make: str) -> str:
        from numpy import savetxt
        current_timestamp = datetime.now().strftime('%d%m%y')
        cls.output_filename = f"{country_short}_{make}_{current_timestamp}.txt"

        dataframe = pd.read_csv(os.path.join(GlobalSettings.acquisiton_folder, filename))

        dataframe.OldPart = dataframe.OldPart.str.replace("-", "")
        dataframe.NewPart = dataframe.NewPart.str.replace("-", "")

        fmt = f"%-13s%-13s%-8s%+15s"
        header = "OldPart      NewPart      ServiceabilityModReason"

        savetxt(fname=os.path.join(GlobalSettings.output_folder, cls.output_filename), X=dataframe, fmt=fmt, encoding='utf-8')

        with open(os.path.join(GlobalSettings.output_folder, cls.output_filename), 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(header)

        return cls.output_filename


