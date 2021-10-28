"""Custom exceptions"""


class ConfigurationError(Exception):
    """Custom configuration exception for configuration manager"""

    def __init__(self, message, errors=None):
        super().__init__(message)
        if errors:
            self.errors = errors


class ApiError(Exception):
    """Custom API Exception"""

    def __init__(self, status, message, errors=None):
        super().__init__(message)
        self.status = status
        self.message = message
        if errors:
            self.errors = errors


class AccessControlError(Exception):
    """Access control exception Exception"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
