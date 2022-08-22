"""User model"""
import datetime
from flask import current_app as app
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload
from src.common.constants import DEFAULT_HASHING_MEMORY_COST
from src.common.helpers import generate_random_string
from src.server import DB
from src.app.auth.models.role import Role


class User(DB.Model):
    """User table definition and supporting database operations"""

    __tablename__ = 'users'

    id = DB.Column(DB.Integer, primary_key=True)
    first_name = DB.Column(DB.String(32), nullable=False)
    last_name = DB.Column(DB.String(32), nullable=False)
    email = DB.Column(DB.String(64), unique=True, nullable=False)
    password = DB.Column(DB.String(128), nullable=False)
    tmp_password = DB.Column(DB.String(128), nullable=True)
    profile_image_url = DB.Column(DB.String(128), nullable=True)
    verification_code = DB.Column(DB.String(4), nullable=True)
    refresh_token = DB.Column(DB.String(512), nullable=True)
    fcm_token = DB.Column(DB.String(256), nullable=True)
    role_id = DB.Column(DB.Integer, DB.ForeignKey('roles.id'), nullable=False)
    status = DB.Column(DB.Integer, nullable=False, default=0)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    role = DB.relationship(
        "Role",
        uselist=False,
        single_parent=True,
        lazy='joined',
        innerjoin=True
    )

    def __init__(self, data):
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.password = self.generate_hash(data.get('password'))
        self.role_id = data.get('role_id')
        self.profile_image_url = data.get(
            'profile_image_url',
            app.config['DEFAULT_PROFILE_IMAGE_URL'])
        self.verification_code = generate_random_string(4)

    # Helper methods
    @staticmethod
    def generate_hash(password):
        """Generates an argon2 password hash"""
        return PasswordHasher(
            memory_cost=DEFAULT_HASHING_MEMORY_COST
        ).hash(password)

    @staticmethod
    def verify_password(password_in_db, provided_password):
        """Calls argon2's verify to check if the provided passwords match"""
        return PasswordHasher(
            memory_cost=DEFAULT_HASHING_MEMORY_COST
        ).verify(password_in_db, provided_password)

    def check_hash(self, password):
        """
        Verifies password hashes match.

        If the verification takes too much time, reduce the
        DEFAULT_HASHING_MEMORY_COST.
        """
        try:
            if self.tmp_password:
                return User.verify_password(self.tmp_password, password)
            return User.verify_password(self.password, password)
        except (VerificationError, VerifyMismatchError):
            return User.verify_password(self.password, password)

    # Database operations
    def save(self):
        """Creates a new user"""
        DB.session.add(self)
        DB.session.commit()

    def update(self, data):
        """
        Updates an existing user

        If password or temporary password values are provided,
        they are hashed before the updating the user
        """
        for key, item in data.items():
            if key in ('password', 'tmp_password'):
                item = self.generate_hash(item)
            setattr(self, key, item)
        self.updated_at = datetime.datetime.utcnow()
        DB.session.commit()

    @staticmethod
    def delete_one(user_id):
        """Deletes a specific user by id"""
        User.query.filter_by(id=user_id).delete()
        DB.session.commit()

    @staticmethod
    def get_many(sort, page=0, per_page=10):
        """
        Get many / all users

        If page is not a non-zero positive number, pagination is disabled
        """
        sort_by = desc if sort[1] == 'desc' else asc
        query = User.query.options(joinedload(
            User.role).joinedload(Role.permissions))
        if page > 0:
            return query.order_by(sort_by(getattr(User, sort[0]))).\
                paginate(per_page=per_page, page=page, error_out=False)
        return query.order_by(sort_by(getattr(User, sort[0]))).all()

    @staticmethod
    def get_one(user_id):
        """
        Get specific user by id, supports sparse fieldsets

        Results contain only the requested columns
        """
        return User.query.options(joinedload(
            User.role).joinedload(Role.permissions)).filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        """Get specific user by email"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(user_id):
        """Get specific user by by"""
        return User.query.filter_by(id=user_id).first()
