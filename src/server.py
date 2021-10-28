import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from src.configuration.manager import setup_configuration
from src.configuration.modules.auth import setup_auth
from src.configuration.modules.logger import setup_logger

API = Api()
DB = SQLAlchemy()
BCRYPT = Bcrypt()
JWT = JWTManager()

def create_app():
    """Initializes app"""
    app = Flask(__name__)
    API.init_app(app=app)
    setup_configuration(app=app)
    setup_auth(app)
    setup_logger(app.config)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'hide_parameters': True, 'convert_unicode': False}

    DB.init_app(app)
    BCRYPT.init_app(app)
    JWT.init_app(app)

    
    return app