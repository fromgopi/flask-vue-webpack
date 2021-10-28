from src.server import DB

class User(DB.Model):
    """User table definition and supporting database operations"""
    
    __tablename__ = 'users'

    id = DB.Column(DB.Integer, primary_key=True)
    first_name = DB.Column(DB.String(32), nullable=False)
    last_name = DB.Column(DB.String(32), nullable=False)
    email = DB.Column(DB.String(64), unique=True, nullable=False)
    password = DB.Column(DB.String(128), nullable=False)
    tmp_password = DB.Column(DB.String(128), nullable=True)
    profile_image_url = DB.Column(DB.String(128), nullable=True)
    verification_code = DB.Column(DB.String(4), nullable=True)
    refresh_token = DB.Column(DB.String(512), nullable=True)
    fcm_token = DB.Column(DB.String(256), nullable=True)