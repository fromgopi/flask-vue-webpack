"""Access control middleware"""
import json
from functools import wraps
from http import HTTPStatus as http_status
from flask import request, g
from flask_jwt_extended import get_jwt_identity
from src.app.user.models.user import User as UserModel
from src.app.user.schema.user import UserSchema
from src.common.helpers import to_camel_case
from src.common.constants import ACCESS_CONTROL_ACTIONS
from src.common.exceptions import AccessControlError, ApiError
from src.common.response import error as error_response
from src.resources.strings.auth.access_control import (
    MISSING_CUSTOM_HANDLER,
    INCORRECT_USAGE,
    USER_NOT_FOUND,
    NO_PERMISSIONS_CONFIGURED,
    INSUFFICIENT_PERMISSION)


def delete_attribute(attribute, new_attributes):
    """Delete key from dict"""
    if attribute[1:] in new_attributes:
        del new_attributes[attribute[1:]]


def validate_attributes(resources, attributes, resource_name, response):
    """Remove restricted attributes and build a new response dict"""
    for resource in resources:
        new_attributes = {}
        for attribute in attributes:
            attribute = to_camel_case(attribute)
            if attribute[0] == '*':
                new_attributes = resource
            elif attribute[0] == '!':
                delete_attribute(attribute, new_attributes)
            else:
                if attribute in resource:
                    new_attributes[attribute] = resource.get(attribute)
        response['data'][resource_name].append(new_attributes)
    return response


def filter_attributes(response):
    """
    Filters response to remove attributes that aren't accessible to the user.
    Runs after all requests.

    Access control attributes aren't filtered at the database layer yet
    """
    if 'ac_attributes' in g and response.status_code != http_status.NO_CONTENT:
        attributes = g.ac_attributes
        resource_name = g.resource_name
        response_json = json.loads(response.get_data())

        if 'data' not in response_json:
            return response
        if resource_name[:len(resource_name)-1] in response_json['data']:
            resource_name = resource_name[:len(resource_name)-1]

        modified_response = {'data': {resource_name: []}}
        resources = response_json['data'][resource_name]

        if not isinstance(response_json['data'][resource_name], list):
            resources = [response_json['data'][resource_name]]

        modified_response = validate_attributes(
            resources, attributes, resource_name, modified_response)
        if 'meta' in response_json:
            modified_response['meta'] = response_json['meta']
        response.set_data(json.dumps(modified_response))
    return response


def default_custom_handler():
    """Fallback default handler for custom access actions"""
    raise AccessControlError(MISSING_CUSTOM_HANDLER)


def validate_permissions(resource, user, identity, custom_handler):
    """
    Handles parsing and validating resource actions.

    Custom handlers are called to validate accesss for custom actions

    If an action on a resource is allowed, user identity, permission and resource
    information are stored in the flask global g to be used by filter_attributes
    """
    for permission in user['role']['permissions']:
        resource_action = permission['action'].split(':')
        if permission['resource'] in [resource, '*'] and \
                resource_action[0] in [ACCESS_CONTROL_ACTIONS[request.method], '*']:
            if(resource_action[1] not in ('any', '*')) and \
                    not custom_handler(identity, user):
                return False
            g.user = identity
            g.ac_attributes = permission['attributes'].replace(
                ' ', '').split(',')
            g.resource_name = resource
            return True
    return False


def access_control(resource_override=None, custom_handler=default_custom_handler):
    """
    Access control decorator
    resource_override - Used instead of flask request information to get the resource
    """
    def actual(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                identity = get_jwt_identity()
                if identity is None:
                    raise AccessControlError(INCORRECT_USAGE)
                user = UserModel.get_one(identity['id'])
                if not user:
                    raise ApiError(http_status.NOT_FOUND, USER_NOT_FOUND)
                user = UserSchema().dump(user)
                if not user['role']['permissions']:
                    raise ApiError(http_status.FORBIDDEN,
                                NO_PERMISSIONS_CONFIGURED)
                resource = resource_override
                if resource is None:
                    resource = request.blueprint
                if validate_permissions(resource, user, identity, custom_handler):
                    return function(*args, **kwargs)
                raise ApiError(http_status.FORBIDDEN,
                            INSUFFICIENT_PERMISSION)
            except (AccessControlError, ApiError) as error:
                return error_response(error.message, error.status)
        return wrapper
    return actual
