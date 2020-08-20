import configparser
import os


class LocalizationProcessingSettings:
    def __init__(self, config_filename: str):
        config = configparser.ConfigParser()
        config.read(os.path.join('app/config/localization', config_filename))

        self.alternative_parts = config['COUNTRY_SETTINGS']['alternative_parts']
        self.alternative_parts_column_index = config['COUNTRY_SETTINGS']['alternative_parts_column_index']

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
        self.decimal_places = config['COUNTRY_SETTINGS']['decimal_places']

        self.vat_setting = config['COUNTRY_SETTINGS']['vat_setting']
        self.vat_value = config['COUNTRY_SETTINGS']['vat_value']

        self.column_titles = config['COUNTRY_SETTINGS']['column_titles']
        self.add_id_column = config['COUNTRY_SETTINGS']['add_id_column']

        self.header = config['COUNTRY_SETTINGS']['header']
        self.names = config['COUNTRY_SETTINGS']['names']
        self.index_col = config['COUNTRY_SETTINGS']['index_col']
        self.skiprows = int(config['COUNTRY_SETTINGS']['skiprows'])
        self.columns_to_use = config['COUNTRY_SETTINGS']['columns_to_use']

        self.partno_start = config['COUNTRY_SETTINGS']['partno_start']
        self.partno_end = config['COUNTRY_SETTINGS']['partno_end']
        self.position_alternative_part = config['COUNTRY_SETTINGS']['position_alternative_part']
        self.position_price = config['COUNTRY_SETTINGS']['position_price']
        self.price_length = config['COUNTRY_SETTINGS']['price_length']
