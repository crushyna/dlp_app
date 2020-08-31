from dataclasses import dataclass
import os
import pandas as pd
from tabulate import tabulate


@dataclass
class GlobalSettings:
    acquisiton_folder = "app/acquisition/"
    localization_folder = "app/config/localization"


class MainProgramHelper:

    @staticmethod
    def check_if_files_exist(filename: str, settings_file: str):
        if not os.path.isfile(os.path.join(GlobalSettings.acquisiton_folder, filename)):
            return f"File {filename} does not exist!"
            # typer.echo(f"File {filename} does not exist!")
            # raise typer.Exit()

        elif not os.path.isfile(os.path.join(GlobalSettings.localization_folder, settings_file)):
            return f"Settings file {settings_file} does not exist!"

            # typer.echo(f"Settings file {settings_file} does not exist!")
            # raise typer.Exit()

        else:
            return True


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