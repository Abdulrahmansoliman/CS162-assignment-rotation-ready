import os
from app.config.base import Config


class Production(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost/minerva_db'
    )
    DEBUG = False
    TESTING = False
