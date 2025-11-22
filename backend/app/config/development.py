import os
from app.config.base import Config


class Development(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    DEBUG = True
    TESTING = False
