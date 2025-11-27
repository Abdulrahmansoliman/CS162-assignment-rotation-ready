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
    VERIFICATION_CODE_MAX_ATTEMPTS = 5
    
    # Rate Limiting for Verification Codes
    VERIFICATION_CODE_MAX_PER_HOUR = 3
    VERIFICATION_CODE_RATE_LIMIT_WINDOW_MINUTES = 60

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 30 * 60  # 30 minutes
    JWT_ALGORITHM = 'HS256'
