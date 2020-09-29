import configparser
import os

from helpers.helpers import GlobalSettings


class LocalizationProcessingSettings:
    def __init__(self, config_filename: str):
        config = configparser.ConfigParser()
        config.read(os.path.join(GlobalSettings.localization_folder, config_filename))

        for each_element in config.items('COUNTRY_SETTINGS'):
            if each_element[1] == 'None':
                setattr(self, each_element[0], None)

            elif each_element[1] == '':
                setattr(self, each_element[0], None)

            elif each_element[1].isdigit():
                setattr(self, each_element[0], int(each_element[1]))

            elif each_element[0] == 'columns_to_use':
                try:
                    setattr(self, each_element[0], tuple(int(num) for num in each_element[1].replace('(', '')
                                                         .replace(')', '')
                                                         .replace('...', '').split(', ')))
                except ValueError:
                    setattr(self, each_element[0], tuple(str(x) for x in each_element[1].replace('(', '')
                                                         .replace(')', '')
                                                         .replace('...', '').split(', ')))
            elif each_element[0] == 'columns_input_names':
                setattr(self, each_element[0], tuple(str(x) for x in each_element[1].replace('(', '')
                                                     .replace(')', '')
                                                     .replace('...', '').split(', ')))
            elif each_element[0] == 'columns_output_names':
                setattr(self, each_element[0], tuple(str(x) for x in each_element[1].replace('(', '')
                                                     .replace(')', '')
                                                     .replace('...', '').split(', ')))

            else:
                setattr(self, each_element[0], each_element[1])
