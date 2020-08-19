import typer
from config.config_parser import LocalizationProcessingSettings


def main(
        country: str = typer.Argument(..., help="Country name"),
        manufacturer: str = typer.Argument(..., help="Manufacturer name"),
        filename: str = typer.Argument(..., help="Filename to process. DO NOT enter filepath!"),
        ):
    typer.echo(f"{country}, {manufacturer}, {filename}")
    processing_settings = LocalizationProcessingSettings('ua_default.ini')
    typer.echo(processing_settings.__dict__)


if __name__ == '__main__':
    typer.run(main)
