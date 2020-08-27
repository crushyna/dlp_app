import configparser
import os


class LocalizationProcessingSettings:
    def __init__(self, config_filename: str):
        config = configparser.ConfigParser()
        config.read(os.path.join('app/config/localization', config_filename))

        self.country_name = config['COUNTRY_SETTINGS']['country_name']
        self.country_short = config['COUNTRY_SETTINGS']['country_short']
        self.make = config['COUNTRY_SETTINGS']['make']

        self.alternative_parts = int(config['COUNTRY_SETTINGS']['alternative_parts'])
        self.alternative_parts_column_index = int(config['COUNTRY_SETTINGS']['alternative_parts_column_index'])

        self.zero_prices = int(config['COUNTRY_SETTINGS']['zero_prices'])
        self.null_price_alternative_parts = int(config['COUNTRY_SETTINGS']['null_price_alternative_parts'])
        self.alternative_equals_original = int(config['COUNTRY_SETTINGS']['alternative_equals_original'])
        self.null_part_number = int(config['COUNTRY_SETTINGS']['null_part_number'])

        self.loop_1 = int(config['COUNTRY_SETTINGS']['loop_1'])
        self.loop_2 = int(config['COUNTRY_SETTINGS']['loop_2'])

        self.part_number_duplicates = int(config['COUNTRY_SETTINGS']['part_number_duplicates'])
        self.prefer_higher_price = int(config['COUNTRY_SETTINGS']['prefer_higher_price'])

        self.price_difference = int(config['COUNTRY_SETTINGS']['price_difference'])

        self.internationalize_characters = int(config['COUNTRY_SETTINGS']['internationalize_characters'])
        self.decimal_places = int(config['COUNTRY_SETTINGS']['decimal_places'])

        self.vat_setting = int(config['COUNTRY_SETTINGS']['vat_setting'])
        self.vat_value = int(config['COUNTRY_SETTINGS']['vat_value'])

        self.column_titles = int(config['COUNTRY_SETTINGS']['column_titles'])
        self.add_id_column = int(config['COUNTRY_SETTINGS']['add_id_column'])

        self.header = config['COUNTRY_SETTINGS']['header']
        self.names = config['COUNTRY_SETTINGS']['names']
        self.index_col = config['COUNTRY_SETTINGS']['index_col']
        self.skiprows = int(config['COUNTRY_SETTINGS']['skiprows'])
        self.columns_to_use = config['COUNTRY_SETTINGS']['columns_to_use']

        self.partno_start = int(config['COUNTRY_SETTINGS']['partno_start'])
        self.partno_end = int(config['COUNTRY_SETTINGS']['partno_end'])
        self.position_alternative_part_start = int(config['COUNTRY_SETTINGS']['position_alternative_part_start'])
        self.position_alternative_part_end = int(config['COUNTRY_SETTINGS']['position_alternative_part_end'])
        self.position_price_start = int(config['COUNTRY_SETTINGS']['position_price_start'])
        self.position_price_end = int(config['COUNTRY_SETTINGS']['position_price_end'])
        self.price_length = int(config['COUNTRY_SETTINGS']['price_length'])
