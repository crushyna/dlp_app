import typer
from config.config_parser import LocalizationProcessingSettings
from functions.excel_importer import ExcelProcessingObject


def main(
        filename: str = typer.Argument(..., help="Filename to process with extension. DO NOT enter filepath!"),
        settings_file: str = typer.Argument(..., help="Settings filename with extension. DO NOT enter filepath!"),
        ):
    typer.echo(f"Starting file processing: {filename} with settings: {settings_file}")

    if filename.lower().endswith(('.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
        typer.echo("Processing...")
        processed_file = ExcelProcessingObject(filename, settings_file)
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
        typer.echo(f"{filename} file type is not supported!")

    # processing_settings = LocalizationProcessingSettings(settings_file)
    # typer.echo(processing_settings.__dict__)


if __name__ == '__main__':
    typer.run(main)
