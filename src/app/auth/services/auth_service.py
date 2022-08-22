"""Auth Service"""
from http import HTTPStatus as http_status
from hashlib import sha512
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token
)
from marshmallow.utils import EXCLUDE
from src.app.user.models.user import User as UserModel
from src.app.auth.schema.auth import LoginSchema, CommonSchema
from src.common.common import create_token
from src.common.exceptions import ApiError
from src.common.constants import (
    TMP_PASSWORD_LENGTH,
    USER_FORCE_RESET_PASSWORD,
    USER_VERIFIED,
    USER_NOT_VERIFIED)
from src.resources.strings.auth import (
    INCORRECT_CREDENTIALS,
    INVALID_REFRESH_TOKEN,
    NOT_FOUND_ERROR,
    RESET_PASSWORD_EMAIL_SUBJECT,
    SEND_VERIFICATION_CODE_EMAIL_SUBJECT,
    USER_ALREADY_VERIFIED,
    INVALID_VERIFICATION_CODE)
import src.common.response as response

class AuthService:
    """Auth service class"""

    def __init__(self):
        self.login_schema = LoginSchema(unknown=EXCLUDE)
        self.common_schema = CommonSchema(unknown=EXCLUDE)

    def auth(self, request_data):
        """
        If the provided credentials are valid, returns access and
        refresh tokens
        """
        login_data = self.login_schema.load(request_data)
        email = login_data.get('email')

        user = UserModel.get_by_email(email=email)
        if not user:
            raise ApiError(http_status.UNAUTHORIZED, INCORRECT_CREDENTIALS)
        
        # Argon2's verify raises a VerifyMismatchError or
        # VerificationError if the password hash check fails
        user.check_hash(request_data.get('password'))

        user.temp_password = None
        access_token = create_token(type='access', data=user)
        refresh_token = create_token(type='refresh', data=user)
        user.refresh_token = refresh_token
        # Check if the payload has fcm_token. Coming from mobile devices.
        if login_data.get('fcm_token'):
            user.fcm_token = login_data.get('fcm_token')
        
        # Check if the user is verified
        if user.verification_code:
            user.status = USER_NOT_VERIFIED
        else:
            user.status = USER_VERIFIED
        # Save user
        user.save()
        # create a user response json from the login schema
        user = self.login_schema.dump(user)
        user['access_token'] = access_token
        user['refresh_token'] = refresh_token

        return response.success(status=http_status.OK, resource_name='user', resource_data=user)