class Config(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'development key'


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = 'test key'
