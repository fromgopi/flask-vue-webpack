"""User schema"""
from marshmallow import fields, validate
from src.common.transformers import CamelCaseSchema
from src.app.auth.schema.permission import PermissionSchema
from src.resources.strings.user import (
    FIRST_NAME_NOT_PROVIDED,
    FIRST_NAME_INVALID,
    LAST_NAME_NOT_PROVIDED,
    LAST_NAME_INVALID,
    EMAIL_NOT_PROVIDED,
    EMAIL_INVALID,
    PASSWORD_NOT_PROVIDED,
    PASSWORD_INVALID,
    ROLE_NOT_PROVIDED)


class RoleSchema(CamelCaseSchema):
    """Common role schema used for all role endpoints"""
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    permissions = fields.Nested(PermissionSchema, many=True)


class UserSchema(CamelCaseSchema):
    """Common user schema used for all user endpoints"""
    id = fields.Int(dump_only=True)
    first_name = fields.Str(
        required=True,
        error_messages={"required": FIRST_NAME_NOT_PROVIDED},
        validate=validate.Length(min=1, error=FIRST_NAME_INVALID))
    last_name = fields.Str(
        required=True,
        error_messages={"required": LAST_NAME_NOT_PROVIDED},
        validate=validate.Length(min=1, error=LAST_NAME_INVALID))
    email = fields.Email(
        required=True,
        error_messages={
            "required": EMAIL_NOT_PROVIDED,
            "invalid": EMAIL_INVALID
        })
    password = fields.Str(
        required=True,
        error_messages={"required": PASSWORD_NOT_PROVIDED},
        load_only=True,
        validate=validate.Length(min=32, error=PASSWORD_INVALID))
    tmp_password = fields.Str(load_only=True)
    profile_image_url = fields.Str()
    verification_code = fields.Str()
    role_id = fields.Int(
        required=True,
        error_messages={"required": ROLE_NOT_PROVIDED})
    role = fields.Nested(RoleSchema, dump_only=True)
    status = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)