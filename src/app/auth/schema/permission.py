"""Permission schema"""
from marshmallow import fields, validate
from src.common.transformers import CamelCaseSchema
from src.resources.strings.auth import (
    PERMISSION_RESOURCE_NOT_PROVIDED,
    PERMISSION_RESOURCE_INVALID,
    PERMISSION_ACTION_NOT_PROVIDED,
    PERMISSION_ATTRIBUTES_NOT_PROVIDED,
    PERMISSION_ROLE_NOT_PROVIDED)


class PermissionSchema(CamelCaseSchema):
    """Common role schema used for all role endpoints"""
    id = fields.Int(dump_only=True)
    resource = fields.Str(
        required=True,
        error_messages={
            "required": PERMISSION_RESOURCE_NOT_PROVIDED
        },
        validate=validate.Length(min=2, error=PERMISSION_RESOURCE_INVALID))
    action = fields.Str(
        required=True,
        error_messages={
            "required": PERMISSION_ACTION_NOT_PROVIDED
        })
    attributes = fields.Str(
        required=True,
        error_messages={
            "required": PERMISSION_ATTRIBUTES_NOT_PROVIDED
        })
    role_id = fields.Int(
        required=True,
        error_messages={
            "required": PERMISSION_ROLE_NOT_PROVIDED
        })
    status = fields.Int()