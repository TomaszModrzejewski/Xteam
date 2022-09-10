import os
from   os import environ

class Config(object):

    DEBUG = False
    TESTING = False

    basedir    = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = 'goh15'

    DB_NAME = "goh15-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "goh15"

    UPLOADS = "/home/username/app/app/static/uploads"

    SESSION_COOKIE_SECURE = True
    DEFAULT_THEME = None


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "goh15-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "goh15"

    UPLOADS = "/home/username/app/app/static/uploads"
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    DEBUG = True

    DB_NAME = "gph15-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "goh15"

    UPLOADS = "/home/username/app/app/static/uploads"
    SESSION_COOKIE_SECURE = False


class DebugConfig(Config):
    DEBUG = False
