"""Role schema"""
from marshmallow import fields, validate
from src.common.transformers import CamelCaseSchema
from src.app.auth.schema.permission import PermissionSchema
from src.resources.strings.auth import (
    ROLE_NAME_NOT_PROVIDED, ROLE_NAME_INVALID)


class UserSchema(CamelCaseSchema):
    """Common user schema used for all user endpoints"""
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    profile_image_url = fields.Str()
    verification_code = fields.Str()
    role_id = fields.Int()
    status = fields.Int()


class RoleSchema(CamelCaseSchema):
    """Common role schema used for all role endpoints"""
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        error_messages={
            "required": ROLE_NAME_NOT_PROVIDED,
        },
        validate=validate.Length(min=2, error=ROLE_NAME_INVALID)
    )
    users = fields.Nested(UserSchema, many=True)
    permissions = fields.Nested(PermissionSchema, many=True)
    status = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)