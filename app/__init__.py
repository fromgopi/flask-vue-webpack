# pylint: unresolved-import, import-error
import logging
import os
import sys

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

from app.databases import initialize_db

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
DOTENV_PATH = os.path.join(APP_ROOT, '.env')


def create_app():
    app = Flask(__name__)
    load_dotenv(DOTENV_PATH)
    load_config(app)
    initialize_db(app)
    api = Api(app)
    load_resources(api=api)
    set_logger(app)
    return app


def load_config(app):
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')
    app.config['APPLICATION_ROOT'] = os.getenv('APP_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MONGODB_DB'] = os.getenv('MONGODB_DB')
    app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST')
    app.config['MONGODB_PORT'] = int(os.getenv('MONGODB_PORT'))
    app.config['MONGODB_USERNAME'] = os.getenv('MONGODB_USERNAME')
    app.config['MONGODB_PASSWORD'] = os.getenv('MONGODB_PASSWORD')


def load_resources(api):
    from app.resources import initialize_routes
    initialize_routes(api)


def set_logger(app):
    """
    Sets logger instance.

    :param app: Flask app instance.
    :return: None
    """
    import logging.handlers
    if app.env == 'development':
        handler = logging.handlers.RotatingFileHandler('logs.log', maxBytes=1024 * 1024)
        # handler = logging.StreamHandler(sys.stdout)
        # logging.getLogger('werkzeug').setLevel(logging.DEBUG)
        logging.getLogger('flask-backend').setLevel(logging.DEBUG)
        # logging.getLogger('werkzeug').addHandler(handler)
        logging.getLogger('flask-backend').addHandler(handler)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        app.logger.setLevel(logging.WARNING)
        app.logger.addHandler(handler)
    else:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    return None
