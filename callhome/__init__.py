import configparser
import os

basedir = os.path.dirname(__file__)
config = configparser.ConfigParser()
config_file = f"{basedir}/config/config.ini"
config.read(config_file)
