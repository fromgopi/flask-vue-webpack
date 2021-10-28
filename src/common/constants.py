"""All constants are placed here."""
import os

ENV_PATH = os.path.join(os.path.dirname(__file__), '../..', '.env')
DEFAULT_PORT = 3000

DEFAULT_HASHING_MEMORY_COST = 102400

# Temporary passwords
TMP_PASSWORD_LENGTH = 7

# Pagination
DISABLE_PAGINATION = 0
DEFAULT_PAGE_LIMIT = 10

# User status
USER_NOT_VERIFIED = 0
USER_VERIFIED = 1
USER_FORCE_RESET_PASSWORD = 2

# ACL actions mapping
ACCESS_CONTROL_ACTIONS = {
    'POST': 'create',
    'PUT': 'replace',
    'PATCH': 'update',
    'GET': 'read',
    'DELETE': 'delete',
    '*': '*'
}