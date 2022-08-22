"""Role model"""
import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload
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

    def __init__(self, data):
        self.name = data.get('name')
        self.status = data.get('status')

    # Database operations
    def save(self):
        """Creates a new role"""
        DB.session.add(self)
        DB.session.commit()

    def update(self, data):
        """
        Updates an existing role

        If password or temporary password values are provided,
        they are hashed before the updating the role
        """
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = datetime.datetime.utcnow()
        DB.session.commit()

    @staticmethod
    def delete_one(role_id):
        """Deletes a specific role by id"""
        Role.query.filter_by(id=role_id).delete()
        DB.session.commit()

    @staticmethod
    def get_many(sort, page=0, per_page=10):
        """
        Get many / all roles

        If page is not a non-zero positive number, pagination is disabled
        """
        sort_by = desc if sort[1] == 'desc' else asc
        query = Role.query.options(joinedload(Role.permissions))
        if page > 0:
            return query.order_by(sort_by(getattr(Role, sort[0]))).\
                paginate(per_page=per_page, page=page)
        return query.order_by(sort_by(getattr(Role, sort[0]))).all()

    @staticmethod
    def get_one(role_id):
        """
        Get specific role by id, supports sparse fieldsets

        Results contain only the requested columns
        """
        return Role.query.options((joinedload(Role.permissions))).filter_by(id=role_id).first()

    @staticmethod
    def get_by_name(role_name):
        """Get specific role by name"""
        return Role.query.filter_by(name=role_name).first()

    @staticmethod
    def get_by_id(role_id):
        """Get specific role by id"""
        return Role.query.filter_by(id=role_id).first()