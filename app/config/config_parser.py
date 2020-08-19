import configparser
import os


class LocalizationProcessingSettings:
    def __init__(self, config_filename: str):
        config = configparser.ConfigParser()
        config.read(os.path.join('app/config/localization', config_filename))

        self.alternative_parts = config['COUNTRY_SETTINGS']['alternative_parts']
        self.zero_prices = config['COUNTRY_SETTINGS']['zero_prices']
        self.null_price_alternative_parts = config['COUNTRY_SETTINGS']['null_price_alternative_parts']
        self.alternative_equals_original = config['COUNTRY_SETTINGS']['alternative_equals_original']
        self.null_part_number = config['COUNTRY_SETTINGS']['null_part_number']
        self.loop_1 = config['COUNTRY_SETTINGS']['loop_1']
        self.loop_2 = config['COUNTRY_SETTINGS']['loop_2']
        self.part_number_duplicates = config['COUNTRY_SETTINGS']['part_number_duplicates']
        self.prefer_higher_price = config['COUNTRY_SETTINGS']['prefer_higher_price']
        self.price_difference = config['COUNTRY_SETTINGS']['price_difference']
        self.internationalize_characters = config['COUNTRY_SETTINGS']['internationalize_characters']
        self.vat_setting = config['COUNTRY_SETTINGS']['vat_setting']
        self.vat_value = config['COUNTRY_SETTINGS']['vat_value']
        self.position_alternative_part = config['COUNTRY_SETTINGS']['position_alternative_part']
        self.position_price = config['COUNTRY_SETTINGS']['position_price']
        self.price_length = config['COUNTRY_SETTINGS']['price_length']


class ManufacturerProcessingSettings:
    def __init__(self, config_filename: str):
        config = configparser.ConfigParser()
        config.read(os.path.join('app/config/localization', config_filename))

        self.alternative_parts = config['COUNTRY_SETTINGS']['alternative_parts']
        self.zero_prices = config['COUNTRY_SETTINGS']['zero_prices']
        self.null_price_alternative_parts = config['COUNTRY_SETTINGS']['null_price_alternative_parts']
        self.alternative_equals_original = config['COUNTRY_SETTINGS']['alternative_equals_original']
        self.null_part_number = config['COUNTRY_SETTINGS']['null_part_number']
        self.loop_1 = config['COUNTRY_SETTINGS']['loop_1']
        self.loop_2 = config['COUNTRY_SETTINGS']['loop_2']
        self.part_number_duplicates = config['COUNTRY_SETTINGS']['part_number_duplicates']
        self.prefer_higher_price = config['COUNTRY_SETTINGS']['prefer_higher_price']
        self.price_difference = config['COUNTRY_SETTINGS']['price_difference']
        self.internationalize_characters = config['COUNTRY_SETTINGS']['internationalize_characters']
        self.vat_setting = config['COUNTRY_SETTINGS']['vat_setting']
        self.vat_value = config['COUNTRY_SETTINGS']['vat_value']
        self.position_alternative_part = config['COUNTRY_SETTINGS']['position_alternative_part']
        self.position_price = config['COUNTRY_SETTINGS']['position_price']
        self.price_length = config['COUNTRY_SETTINGS']['price_length']
