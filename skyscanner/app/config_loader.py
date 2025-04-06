import configparser
import os

class CaseInsensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

config = CaseInsensitiveConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'location_ids.properties')
config.read(config_path)

def get_airport_code(prompt):
    while True:
        code = input(prompt).strip().upper()
        try:
            return config.get('DEFAULT', code), code
        except configparser.NoOptionError:
            valid_codes = ', '.join(config.options('DEFAULT'))
            print(f"Invalid code. Valid options: {valid_codes}\n")

def get_location_id(prompt):
    while True:
        try:
            return config.get('DEFAULT', prompt), prompt
        except configparser.NoOptionError:
            valid_codes = ', '.join(config.options('DEFAULT'))
            print(f"Invalid code. Valid options: {valid_codes}\n")
