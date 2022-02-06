import os


class Config:
    pass


class ConfigProd(Config):
    FLASK_ENV = 'production'
    SECRET_KEY = os.getenv('SECRET_KEY')


class ConfigDev(Config):
    FLASK_ENV = 'development'
    SECRET_KEY = 'secret key'


class ConfigTesting(Config):
    FLASK_ENV = 'testing'
    SECRET_KEY = 'secret key'
    TESTING = True
    WTF_CSRF_ENABLED = False
