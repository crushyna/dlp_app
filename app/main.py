import typer
import logging
from typing import Optional
from helpers.helpers import MainProgramHelper, GlobalSettings
from functions.csv_importer import CSVProcessingObject
from functions.excel_importer import ExcelProcessingObject
import os

__version__ = "0.3.10"

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
    Entry point for application! Provide input filename and settings filename in order to proceed.
    Made by: Radosław Malinowski (https://github.com/crushyna)
    """
    # check if files exits
    result = MainProgramHelper.check_if_files_exist(filename, settings_file)
    if result is True:
        MainProgramHelper.remove_unused_db_files()
        typer.echo(f"Starting file processing: {filename} with settings: {settings_file}")
        logging.info(f"===> Starting file processing: {filename} with settings: {settings_file}")

        if filename.lower().endswith(('.xls', '.xlsx', '.xlsm', '.odf', '.ods', '.odt')):
            logging.debug("Using xlrd engine")
            processed_file = ExcelProcessingObject(filename, settings_file, engine='xlrd')

        elif filename.lower().endswith('.xlsb'):
            logging.debug("Using pyxlsb engine")
            processed_file = ExcelProcessingObject(filename, settings_file, engine='pyxlsb')

        elif filename.lower().endswith(('.csv', '.txt', '.asc')):
            logging.debug("Using standard CSV Python engine")
            processed_file = CSVProcessingObject(filename, settings_file)

        else:
            try:
                typer.echo("File type not recognized! Trying to process as a text file...")
                logging.debug("Using standard CSV Python engine")
                processed_file = CSVProcessingObject(filename, settings_file)

            except FileNotFoundError as er:
                typer.echo(er)
                typer.echo(f"{filename} file type is not supported!")
                logging.critical(f"{filename} file type is not supported!")
                raise typer.Exit()

        # TODO: this has to be moved somewhere else!
        processing_list = [processed_file.drop_duplicates,
                           processed_file.drop_loops,
                           processed_file.create_prices_for_missing_ss,
                           processed_file.drop_zero_prices,
                           processed_file.drop_zero_prices_alternative_parts,
                           processed_file.drop_alternative_equals_original,
                           processed_file.drop_null_part_no,
                           processed_file.drop_na_values,
                           processed_file.vat_setter,
                           processed_file.drop_duplicates]

        if processed_file.save_raw == 1:
            pass

        else:
            try:
                for each_function in processing_list:
                    each_function()

            except Exception as er:
                typer.echo(er)
                logging.critical(er)
                raise typer.Exit()

            output_filename = processed_file.save_to_fwf_txt()
            typer.echo(processed_file.initial_dataframe)
            typer.echo("Starting post-processing")
            logging.info("Starting post-processing")
            processed_file.post_update_timestamp_mark()
            processed_file.post_set_comma_decimal_sep()
            processed_file.post_alternative_float_column()

        typer.echo("Done!")
        logging.info(f"===> {filename} processing finished!")

    else:
        typer.echo(result)
        logging.critical(result)


if __name__ == '__main__':
    typer.run(main)
