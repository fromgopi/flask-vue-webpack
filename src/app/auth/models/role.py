import datetime
from src.server import DB

class Role(DB.Model):
    """Role table definition and supporting database operations"""

    __tablename__ = 'roles'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(128), nullable=False)
    status = DB.Column(DB.Integer, nullable=False, default=0)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    users = DB.relationship("User", backref='user')
    permissions = DB.relationship(
        "Permission", backref='permission', uselist=True, lazy='joined')