"""Flask configuration """


class Config:
    """Set Flsk Config Variables"""
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///userinfo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "thisissecret"

