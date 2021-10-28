"""Package containing all the info."""
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

db = MongoEngine()


def initialize_db(app):
    """
    Initializes Mongoengine Instance.
    :param app: Flask Instance
    :return: None
    """
    db.init_app(app)


from .todo import Todo
