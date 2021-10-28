"""JSON response wrappers"""
from http import HTTPStatus as http_status
import traceback
from flask import json, Response, request


def custom(response, status):
    """Base response wrapper"""
    request.log.info(response)
    return Response(
        mimetype="application/json",
        response=json.dumps(response),
        status=status
    )


# Wrappers
def success(status, resource_name=None, resource_data=None, meta=None):
    """Success response wrapper"""
    # if resource_name is not None:
    response = {'data': {}}
    response['data'][resource_name] = resource_data
    if meta is not None:
        response['meta'] = meta
    return custom(response, status)


def error(errors, status=None):
    """Error response wrapper"""
    messages = str(errors)
    status = getattr(
        errors,
        'status',
        http_status.INTERNAL_SERVER_ERROR
    ) if status is None else status
    # Returns last line of of the stack trace if errors have empty messages
    messages = messages.split('\n')[0] if bool(
        messages) else traceback.format_exc().splitlines()[-1]
    return custom({'errors': {'messages': [messages]}}, status)


# Marshmallow validation errors
def validation_error(errors):
    """Response wrapper for marshmallow's validation error"""
    messages = {}
    for key in errors.messages:
        if '_schema' in errors.messages[key]:
            messages[key] = errors.messages[key]['_schema']
        else:
            messages[key] = errors.messages[key][0]
    return custom({'errors': {'messages': [messages]}},
                  http_status.UNPROCESSABLE_ENTITY)
