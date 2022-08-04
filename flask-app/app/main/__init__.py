from re import A
from flask import Flask
from flask_socketio import SocketIO

from .config import config_nane

socketio = SocketIO()

def create_app(config_name):
    application = Flask(__name__)
    application.config.from_object(config_nane[config_name]())
    # socketio.init_app(application)
    initialize_db_session(application)
    controller_blueprint(application)

    return application

def initialize_db_session(application):
    from app.main.DB_Session.NewSession import DB_Session
    application.config.update({'TEMP_SESSION':DB_Session(url=application.config.get('POSTGRE_DB_URL'),engine_kwargs={'pool_size': 10, 'max_overflow': 5, 'pool_timeout': 10, 'pool_recycle': 3600})})

def controller_blueprint(application):
    from app.main.Controllers.transactions_api import transactions_api

    application.register_blueprint(transactions_api) #, url_prefix='/txn'

