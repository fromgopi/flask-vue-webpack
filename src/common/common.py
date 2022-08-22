"""Common Functions"""
from flask_jwt_extended import create_access_token, create_refresh_token


def create_token(type, data={}) -> str:
    """Utilify function which creates token base on the type."""
    if type is 'access':
        return create_access_token(
            identity= {'id': data.id, 'email': data.email}
        )
    
    if type is 'refresh':
        return create_refresh_token(
            identity={'id': data.id, 'email': data.email}
        )
    
    return ''