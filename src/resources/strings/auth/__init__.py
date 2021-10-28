"""Auth strings"""

# Email
RESET_PASSWORD_EMAIL_SUBJECT = 'Password reset'
SEND_VERIFICATION_CODE_EMAIL_SUBJECT = 'Verification code'

# Endpoint errors
# Auth
INCORRECT_CREDENTIALS = 'Username or password is incorrect'
INVALID_REFRESH_TOKEN = 'Please provide a valid refresh token'
USER_ALREADY_VERIFIED = 'User has already been verified'
INVALID_VERIFICATION_CODE = 'Please provide a valid verification code'
# Roles
NOT_FOUND_ERROR = 'Role not found'
CONFLICT_ERROR = 'Role already exists'

# Validation errors
EMAIL_NOT_PROVIDED = 'Please provide an email address'
EMAIL_INVALID = 'Please provide a valid email address'
PASSWORD_NOT_PROVIDED = 'Please provide a password hash'

ROLE_NAME_NOT_PROVIDED = 'Please provide a role name'
ROLE_NAME_INVALID = 'Role name must contain atleast 2 characters'

PERMISSION_RESOURCE_NOT_PROVIDED = 'Please provide a resource name'
PERMISSION_RESOURCE_INVALID = 'Please provide a valid resource name'
PERMISSION_ACTION_NOT_PROVIDED = 'Please provide an action for this resource'
PERMISSION_ATTRIBUTES_NOT_PROVIDED = 'Please provide attribute permissions'
PERMISSION_ROLE_NOT_PROVIDED = 'Please provide a role id'