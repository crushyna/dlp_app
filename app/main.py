import typer
from config.config_parser import LocalizationProcessingSettings


def main(
        filename: str = typer.Argument(..., help="Filename to process. DO NOT enter filepath!"),
        settings_file: str = typer.Argument(..., help="Settings filename. DO NOT enter filepath!"),
        ):
    typer.echo(f"{filename}, {settings_file}")
    processing_settings = LocalizationProcessingSettings(settings_file)
    typer.echo(processing_settings.__dict__)



if __name__ == '__main__':
    typer.run(main)
