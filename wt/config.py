# -*- coding: utf-8 -*-
import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '51f52814-0071-11e6-a247-000ec6c2372c')

    # Logging
    if "LOGENTRIES_TOKEN" in os.environ.keys():
        LOGENTRIES_TOKEN = os.environ["LOGENTRIES_TOKEN"]
    else:
        LOGENTRIES_TOKEN = None

    CHATFIRST_TOKEN = os.getenv("CHATFIRST_TOKEN", None)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
