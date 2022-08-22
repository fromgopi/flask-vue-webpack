"""Auth Endpoints"""
from flask import Blueprint

AUTH_USER_API = Blueprint('auth', __name__)

@AUTH_USER_API.route('/auth/user/login', method=["POST"])
def login():
    """
    On successful login, returns user information along with access and
    refresh tokens.
    """