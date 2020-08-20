import typer
from config.config_parser import LocalizationProcessingSettings
from functions.excel_importer import ExcelProcessingObject


def main(
        filename: str = typer.Argument(..., help="Filename to process. DO NOT enter filepath!"),
        settings_file: str = typer.Argument(..., help="Settings filename. DO NOT enter filepath!"),
):
    typer.echo(f"Starting file processing: {filename} with settings: {settings_file}")

    if filename.lower().endswith(('.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
        processed_file = ExcelProcessingObject(filename, settings_file)
        typer.echo(processed_file.initial_dataframe)

    else:
        typer.echo(f"{filename} file type is not supported!")

    # processing_settings = LocalizationProcessingSettings(settings_file)
    # typer.echo(processing_settings.__dict__)


if __name__ == '__main__':
    typer.run(main)
