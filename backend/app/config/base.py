"""
Base Configuration
Shared settings across all environments.
"""


import os


class Config:
    """Base configuration with shared settings."""
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Verification Settings
    VERIFICATION_CODE_LENGTH = 6
    VERIFICATION_CODE_EXPIRY_MINUTES = 15
    MAX_VERIFICATION_ATTEMPTS = 5
    
    # Rate Limiting for Verification Codes
    VERIFICATION_CODE_MAX_PER_HOUR = 3
    VERIFICATION_CODE_RATE_LIMIT_WINDOW_MINUTES = 60

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 30 * 60  # 30 minutes
    JWT_ALGORITHM = 'HS256'

    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@rotationready.com')
    MAIL_DEFAULT_SENDER_NAME = os.getenv('MAIL_DEFAULT_SENDER_NAME', 'Rotation Ready')
    
    # Email Feature Flags
    MAIL_ENABLED = os.getenv('MAIL_ENABLED', 'false').lower() == 'true'
    MAIL_SUPPRESS_SEND = os.getenv('MAIL_SUPPRESS_SEND', 'false').lower() == 'true'
    MAIL_DEBUG = os.getenv('MAIL_DEBUG', 'false').lower() == 'true'
