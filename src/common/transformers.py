"""Transformers"""
from marshmallow import Schema
from src.common.helpers import to_camel_case


class CamelCaseSchema(Schema):
    """Transforms request and response keys from snake_case to camelCase"""

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = to_camel_case(field_obj.data_key or field_name)
