"""Flask configuration """

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flsk Config Variables"""

    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Openweather Api
    API_KEY = '84ab8aee3c08e48f02450cc7580714cc'
    API_URL = 'https://api.openweathermap.org/data/2.5/onecall'


class ProdConfig(Config):
    TESTING = False
    DEBUG = False
    FLASK_ENV = 'production'


class DevConfig(Config):
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'
