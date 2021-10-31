import datetime
from sqlalchemy import asc, desc
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

    def __init__(self, data):
        self.resource = data.get('resource')
        self.action = data.get('action')
        self.attributes = data.get('attributes')
        self.role_id = data.get('role_id')
        self.status = data.get('status')
    
    # Database operations.
    def save(self):
        """Create new permission"""
        DB.session.add(self)
        DB.session.commit()

    def update(self, data):
        """
        Updates an existing permission

        If password or temporary password values are provided,
        they are hashed before the updating the permission
        """
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = datetime.datetime.utcnow()
        DB.session.commit()
    
    @staticmethod
    def delete_one(permission_id):
        """Deletes a specific permission by id"""
        Permission.query.filter_by(id=permission_id).delete()
        DB.session.commit()

    
    @staticmethod
    def get_many(columns, sort, page=0, per_page=10):
        """
        Get many / all permissions

        If page is not a non-zero positive number, pagination is disabled
        """
        sort_by = desc if sort[1] == 'desc' else asc
        query = Permission.query.with_entities(
            *[getattr(
                Permission,
                str(columns)
            ) for col in columns]
        )
        if page > 0:
            return query.order_by(
                sort_by(getattr(Permission, sort[0]))).\
                paginate(per_page=per_page, page=page)
        return query.order_by(sort_by(getattr(Permission, sort[0]))).all()
    

    @staticmethod
    def get_one(permission_id, columns):
        """
        Get specific permission by id, supports sparse fieldsets

        Results contain only the requested columns
        """
        return Permission.query.with_entities(
            *[getattr(
                Permission,
                str(column)
            ) for column in columns]).filter_by(id=permission_id).first()

    @staticmethod
    def get_unique(resource, action):
        """Get specific permission by name"""
        return Permission.query.filter_by(resource=resource, action=action).first()

    @staticmethod
    def get_by_id(permission_id):
        """Get specific role by id"""
        return Permission.query.filter_by(id=permission_id).first()