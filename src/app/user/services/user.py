"""User Service"""
from http import HTTPStatus as http_status
import logging
from flask import request, current_app as app
from marshmallow import EXCLUDE
from src.app.user.models.user import User as UserModel
from src.app.user.schema.user import RoleSchema, UserSchema
from src.common.exceptions import ApiError
from src.common.helpers import (
    to_snake_case,
    validate_sparse_fieldsets,
    remove_empty_objects,
    build_pagination_meta
)
import src.common.response as response
import src.resources.strings.user as strings


class UserService:
    """User service class"""
    logger = logging.getLogger(__name__)
    def __init__(self):
        self.user_schema = UserSchema(unknown=EXCLUDE)
        self.users_schema = UserSchema(many=True)
        self.relations = {'roles': RoleSchema}

    # CRUD
    def create_one(self, request_body):
        """
        Create a single user if there are no existing users that have the
        same email address.

        On successful user creation, the user status is set to NOT_VERIFIED
        and an email with a verification code is sent to the registered email
        address.
        """
        user_data = self.user_schema.load(request_body)

        # Check user if already exists. 
        user = UserModel.get_by_email(user_data.get('email'))
        if user:
            raise ApiError(http_status.CONFLICT, strings.CONFLICT_ERROR)
        
        user = UserModel(user_data)
