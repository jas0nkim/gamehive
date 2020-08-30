class DefaultConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://gamehive:gamehive@postgres:5432/gamehive'

class TestingConfig(DefaultConfig):
    DB_URI = 'postgresql://gamehive:gamehive@postgres:5432'
    DATABASE_NAME = 'test_gamehive'
    SQLALCHEMY_DATABASE_URI = 'postgresql://gamehive:gamehive@postgres:5432/test_gamehive'
    TESTING = True
