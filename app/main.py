import typer
from functions.excel_importer import ExcelProcessingObject
from helpers.helpers import MainProgramHelper
import os

from helpers.helpers import GlobalSettings


def main(
        filename: str = typer.Argument(..., help="Filename to process with extension. DO NOT enter filepath!"),
        settings_file: str = typer.Argument(..., help="Settings filename with extension. DO NOT enter filepath!"),
):
    global processed_file
    # check if files exits
    result = MainProgramHelper.check_if_files_exist(filename, settings_file)
    if result is True:

        typer.echo(f"Starting file processing: {filename} with settings: {settings_file}")
        if filename.lower().endswith(('.xls', '.xlsx', '.xlsm', '.odf', '.ods', '.odt')):
            typer.echo("Processing...")
            processed_file = ExcelProcessingObject(filename, settings_file, engine='xlrd')

        elif filename.lower().endswith('.xlsb'):
            typer.echo("Processing...")
            processed_file = ExcelProcessingObject(filename, settings_file, engine='pyxlsb')

        else:
            typer.echo(f"{filename} file type is not supported!")
            raise typer.Exit()

        processed_file.drop_duplicates()
        processed_file.drop_zero_prices()
        processed_file.drop_zero_prices_alternative_parts()
        processed_file.drop_alternative_equals_original()
        processed_file.drop_null_part_no()

        typer.echo("Saving fixed-width file...")
        processed_file.save_to_fwf_txt()
        typer.echo(processed_file.initial_dataframe)

        typer.echo("Done!")

    else:
        typer.echo(result)

    # processing_settings = LocalizationProcessingSettings(settings_file)
    # typer.echo(processing_settings.__dict__)


if __name__ == '__main__':
    typer.run(main)
