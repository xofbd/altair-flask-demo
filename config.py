import os


class Config:
    SECRET_KEY = os.urandom(32)


class ConfigProd(Config):
    FLASK_ENV = 'production'


class ConfigDev(Config):
    FLASK_ENV = 'development'


class ConfigTesting(Config):
    FLASK_ENV = 'testing'
    TESTING = True
    WTF_CSRF_ENABLED = False
