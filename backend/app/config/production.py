import os
from app.config.base import Config


class Production(Config):
    """Production configuration."""
    
    # PostgreSQL database - Render provides DATABASE_URL
    # Fix for Render: they use 'postgres://' but SQLAlchemy needs 'postgresql://'
    _db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/minerva_db')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    
    DEBUG = False
    TESTING = False
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
