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

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
