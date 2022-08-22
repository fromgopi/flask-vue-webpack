"""Auth Schemas"""
from marshmallow import fields
from src.common.transformers import CamelCaseSchema
from src.resources.strings.auth import (
    EMAIL_NOT_PROVIDED, EMAIL_INVALID, PASSWORD_NOT_PROVIDED)


class LoginSchema(CamelCaseSchema):
    """Login schema"""
    id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    fcm_token = fields.Str(load_only=True)
    refresh_token = fields.Str()
    email = fields.Email(
        required=True,
        error_messages={
            "required": EMAIL_NOT_PROVIDED,
            "invalid": EMAIL_INVALID
        }
    )
    password = fields.Str(
        required=True,
        load_only=True,
        error_messages={
            "required": PASSWORD_NOT_PROVIDED
        }
    )
    tmp_password = fields.Str(load_only=True)
    profile_image_url = fields.Str(dump_only=True)
    verification_code = fields.Str(load_only=True)
    status = fields.Int(dump_only=True)


class CommonSchema(CamelCaseSchema):
    """Common schema used for most auth endpoints"""
    id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    email = fields.Email(
        required=True,
        error_messages={
            "required": EMAIL_NOT_PROVIDED,
            "invalid": EMAIL_INVALID
        }
    )
    verification_code = fields.Str(dump_only=True)
    status = fields.Int(dump_only=True)
