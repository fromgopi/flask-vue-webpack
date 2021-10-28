"""Auth configuration"""
from datetime import timedelta

def setup_auth(app):
    """Auth configuration"""
    # Convert to seconds
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(
        seconds=int(app.config['AUTH_TOKEN_EXPIRY'])*60)