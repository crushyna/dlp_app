from dataclasses import dataclass

import pandas as pd
from tabulate import tabulate


@dataclass
class GlobalSettings:
    acquisiton_folder = "app/acquisition/"
    localization_folder = "app/config/localization"


class SaveTxtHelper:

    @staticmethod
    def to_fwf(df, fname):
        content = tabulate(df.values.tolist(), list(df.columns), tablefmt="plain")
        open(fname, "w").write(content)

    pd.DataFrame.to_fwf = to_fwf

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
