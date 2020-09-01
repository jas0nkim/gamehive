import io
import configparser

config = configparser.ConfigParser()
# add a fake section [POSTGRES]
config.read_string('[POSTGRES]\n' + open('/postgres.env', 'r').read())

class DefaultConfig(object):
    SQLALCHEMY_DATABASE_URI = f'postgresql://{config["POSTGRES"]["POSTGRES_USER"]}:{config["POSTGRES"]["POSTGRES_PASSWORD"]}@postgres:5432/gamehive'

class TestingConfig(DefaultConfig):
    DB_URI = f'postgresql://{config["POSTGRES"]["POSTGRES_USER"]}:{config["POSTGRES"]["POSTGRES_PASSWORD"]}@postgres:5432'
    DATABASE_NAME = 'test_gamehive'
    SQLALCHEMY_DATABASE_URI = 'postgresql://gamehive:gamehive@postgres:5432/test_gamehive'
    TESTING = True
