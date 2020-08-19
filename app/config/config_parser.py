import configparser
import os


class LocalizationProcessingSettings:
    def __init__(self, config_filename: str):
        config = configparser.ConfigParser()
        config.read(os.path.join('app/config/localization', config_filename))

        self.alternative_parts = config['SETTINGS']['alternative_parts']
        self.zero_prices = config['SETTINGS']['zero_prices']
        self.null_price_alternative_parts = config['SETTINGS']['null_price_alternative_parts']
        self.alternative_equals_original = config['SETTINGS']['alternative_equals_original']
        self.null_part_number = config['SETTINGS']['null_part_number']
        self.loop_1 = config['SETTINGS']['loop_1']
        self.loop_2 = config['SETTINGS']['loop_2']
        self.part_number_duplicates = config['SETTINGS']['part_number_duplicates']
        self.prefer_higher_price = config['SETTINGS']['prefer_higher_price']
        self.price_difference = config['SETTINGS']['price_difference']
        self.internationalize_characters = config['SETTINGS']['internationalize_characters']
        self.vat_setting = config['SETTINGS']['vat_setting']
        self.vat_value = config['SETTINGS']['vat_value']
