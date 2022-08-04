from distutils.log import debug
import os
import urllib.parse

class Config:
    debug=False
    SECRET_KEY = 'c219d4e3-3ea8-4dbb-8641-8bbfc644aa18'
    # SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False    

class DevelopmentConfig(Config):
    def __init__(self):
        self.APP_ENV = 'development'
        self.DEVELOPMENT = True
        self.DEBUG = True
        self.SECRET_KEY = 'Test@APIS$PayNearby'
        self.FILE_PATH = 'C:\\csv'
        # self.postgre_db_url = '{dialect}://{user}:{password}@{host}:{port}/{database}'
        self.POSTGRE_DB_URL = 'postgres://postgres:root@127.0.0.1:5433/assignment'

config_nane = dict(
    development=DevelopmentConfig
)