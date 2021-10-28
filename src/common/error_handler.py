"""Error Handlers"""
from http import HTTPStatus as http_status
from flask import jsonify

# Route error handlers
def format_errors(status, errors):
    """Converts errors to standard json error format"""
    return jsonify(
        {'errors': {'messages': [str(errors)]}}
    ), status


def bad_request_handler(errors):
    """400 route handler"""
    return format_errors(http_status.BAD_REQUEST, errors)


def not_found_handler(errors):
    """404 route handler"""
    return format_errors(http_status.NOT_FOUND, errors)


def method_not_allowed_handler(errors):
    """405 route handler"""
    return format_errors(http_status.METHOD_NOT_ALLOWED, errors)


# Register route handlers
def register_route_error_handlers(app):
    """Sets up route error handlers"""
    app.register_error_handler(http_status.BAD_REQUEST, bad_request_handler)
    app.register_error_handler(http_status.NOT_FOUND, not_found_handler)
    app.register_error_handler(
        http_status.METHOD_NOT_ALLOWED, method_not_allowed_handler)


# Auth error handlers
def expired_token_handler():
    """Expired token error handler"""
    return jsonify({'errors': {'messages': ['Authorization token has expired']}}), 401


def common_auth_handler(errors):
    """Handles multiple auth errors"""
    return jsonify({'errors': {'messages': [str(errors)]}}), 401


# Register auth handlers
def register_auth_error_handlers(jwt):
    """Sets up auth error handlers"""
    jwt.expired_token_loader(expired_token_handler)
    jwt.unauthorized_loader(common_auth_handler)
    jwt.invalid_token_loader(common_auth_handler)