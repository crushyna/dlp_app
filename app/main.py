import typer
import logging
from typing import Optional
from functions.csv_importer import CSVProcessingObject
from functions.excel_importer import ExcelProcessingObject
from helpers.helpers import MainProgramHelper, GlobalSettings
import os

__version__ = "0.2.3"

if GlobalSettings.use_logs == 1:
    logging.basicConfig(filename=os.path.join('app/logs', 'application.log'), level=GlobalSettings.logging_level,
                        format='%(asctime)s.%(msecs)03d : %(levelname)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

if GlobalSettings.return_console_messages == 0:
    def _disable_console_messages(*args, **kwargs):
        pass


    typer.echo = _disable_console_messages


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
    """
    Entry point for application!
    :param filename:
    :param settings_file:
    :param version
    """
    # check if files exits
    result = MainProgramHelper.check_if_files_exist(filename, settings_file)
    if result is True:

        typer.echo(f"Starting file processing: {filename} with settings: {settings_file}")
        logging.info(f"Starting file processing: {filename} with settings: {settings_file}")

        if filename.lower().endswith(('.xls', '.xlsx', '.xlsm', '.odf', '.ods', '.odt')):
            typer.echo("Processing...")
            logging.debug("Using xlrd engine")
            processed_file = ExcelProcessingObject(filename, settings_file, engine='xlrd')

        elif filename.lower().endswith('.xlsb'):
            typer.echo("Processing...")
            logging.debug("Using pyxlsb engine")
            processed_file = ExcelProcessingObject(filename, settings_file, engine='pyxlsb')

        elif filename.lower().endswith(('.csv', '.txt')):
            typer.echo("Processing...")
            logging.debug("Using standard CSV Python engine")
            processed_file = CSVProcessingObject(filename, settings_file)

        else:
            typer.echo(f"{filename} file type is not supported!")
            logging.critical(f"{filename} file type is not supported!")
            raise typer.Exit()

        processing_list = [processed_file.drop_duplicates,
                           processed_file.drop_zero_prices,
                           processed_file.drop_zero_prices_alternative_parts,
                           processed_file.drop_alternative_equals_original,
                           processed_file.drop_null_part_no,
                           processed_file.drop_na_values,
                           processed_file.vat_setter]

        for each_function in processing_list:
            each_function()

        typer.echo("Saving fixed-width file...")
        processed_file.save_to_fwf_txt()
        typer.echo(processed_file.initial_dataframe)

        typer.echo("Done!")
        logging.info(f"{filename} processing finished!")

    else:
        typer.echo(result)
        logging.critical(result)


if __name__ == '__main__':
    typer.run(main)
