import os
from app.config.base import Config


class Development(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    DEBUG = True
    TESTING = False
    ENV = 'development'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 30 * 60  # 30 minutes
    JWT_ALGORITHM = 'HS256'
