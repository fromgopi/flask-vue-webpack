class SchemaValidationError(Exception):
    pass

errors = {
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    }
}