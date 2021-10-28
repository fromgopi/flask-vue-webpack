import datetime
from src.server import DB

class Permission(DB.Model):
    """Permission table definition and supporting database operations"""

    __tablename__ = 'permissions'

    id = DB.Column(DB.Integer, primary_key=True)
    resource = DB.Column(DB.String(32), nullable=False)
    action = DB.Column(DB.String(20), nullable=False)
    attributes = DB.Column(DB.String(256), nullable=False)
    role_id = DB.Column(DB.Integer, DB.ForeignKey('roles.id'), nullable=False)
    status = DB.Column(DB.Integer, nullable=False, default=1)
    role = DB.relationship(
        "Role",
        uselist=False,
        single_parent=True,
        lazy='noload',
        innerjoin=True
    )
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())