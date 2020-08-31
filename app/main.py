from typing import Optional
import typer
from functions.excel_importer import ExcelProcessingObject
from helpers.helpers import MainProgramHelper

__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        typer.echo(f"Data Localization Processing App version: {__version__}")
        raise typer.Exit()


def main(
        filename: str = typer.Argument(...,
                                       help="Filename to process including its extension. DO NOT enter filepath!"),
        settings_file: str = typer.Argument(...,
                                            help="Settings filename including its extension. DO NOT enter filepath!"),
        version: Optional[bool] = typer.Option(
            None, "--version", callback=version_callback
        )
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

        processing_list = [processed_file.drop_duplicates,
                           processed_file.drop_zero_prices,
                           processed_file.drop_zero_prices_alternative_parts,
                           processed_file.drop_alternative_equals_original,
                           processed_file.drop_null_part_no]

        for each_function in processing_list:
            each_function()

        typer.echo("Saving fixed-width file...")
        processed_file.save_to_fwf_txt()
        typer.echo(processed_file.initial_dataframe)

        typer.echo("Done!")

    else:
        typer.echo(result)


if __name__ == '__main__':
    typer.run(main)
