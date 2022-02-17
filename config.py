import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    URI_DB = os.getenv("URI_DB")


class ConfigProd(Config):
    FLASK_ENV = "production"
    SECRET_KEY = os.getenv("SECRET_KEY")


class ConfigDev(Config):
    FLASK_ENV = "development"
    SECRET_KEY = "secret key"


class ConfigTesting(Config):
    FLASK_ENV = "testing"
    SECRET_KEY = "secret key"
    TESTING = True
    WTF_CSRF_ENABLED = False
    URI_DB = "sqlite:///tests/data/wells_test.db"
