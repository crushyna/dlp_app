import configparser
from dataclasses import dataclass
import os


@dataclass
class GlobalSettings:
    config = configparser.ConfigParser()
    config.read('app/config/global_settings.ini')

    # TODO: delete str_* as they shouldn't be used
    acquisiton_folder = config['GLOBAL_APP_SETTINGS']['acquisiton_folder']
    localization_folder = config['GLOBAL_APP_SETTINGS']['localization_folder']
    str_part_no = config['GLOBAL_APP_SETTINGS']['str_part_no']
    str_part_ss = config['GLOBAL_APP_SETTINGS']['str_part_ss']
    str_price = config['GLOBAL_APP_SETTINGS']['str_price']
    return_console_messages = int(config['GLOBAL_APP_SETTINGS']['return_console_messages'])
    use_logs = int(config['GLOBAL_APP_SETTINGS']['use_logs'])
    logging_level = int(config['GLOBAL_APP_SETTINGS']['logging_level'])


class MainProgramHelper:

    @staticmethod
    def check_if_files_exist(filename: str, settings_file: str):
        if not os.path.isfile(os.path.join(GlobalSettings.acquisiton_folder, filename)):
            return f"File {filename} does not exist!"

        elif not os.path.isfile(os.path.join(GlobalSettings.localization_folder, settings_file)):
            return f"Settings file {settings_file} does not exist!"

        else:
            return True


class SaveTxtHelper:

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
