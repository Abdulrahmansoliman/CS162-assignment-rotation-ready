from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
import os
import logging
import sys

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()


def setup_logging(app):
    """Configure structured logging to stdout"""
    # Remove default Flask handlers
    app.logger.handlers.clear()
    
    # Create stdout handler
    handler = logging.StreamHandler(sys.stdout)
    
    # Set format based on environment
    if app.config.get('ENV') == 'production':
        # JSON-like format for production
        formatter = logging.Formatter(
            '{"time":"%(asctime)s", "level":"%(levelname)s", '
            '"name":"%(name)s", "message":"%(message)s"}'
        )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
    
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    
    # Set log level from config or default to INFO
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    app.logger.setLevel(getattr(logging, log_level))
    
    # Log startup
    app.logger.info(f'Application starting in {app.config.get("ENV", "development")} mode')


def create_app(config_name='development'):
    """Application factory function."""
    from app.config.production import Production
    from app.config.testing import Testing
    from app.config.development import Development
    
    app = Flask(__name__)
    
    # Load configuration based on environment
    if config_name == 'production':
        app.config.from_object(Production)
    elif config_name == 'testing':
        app.config.from_object(Testing)
    else:
        app.config.from_object(Development)
    
    # Setup logging
    setup_logging(app)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    
    # Enable CORS with configurable origins
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    CORS(app, resources={
        r"/api/*": {
            "origins": cors_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints and JWT handlers
    from app.api.v1 import api_bp
    from app.api.v1.auth import jwt_handlers
    
    app.register_blueprint(api_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        app.logger.info('Database tables created/verified')
    
    app.logger.info(f'Application initialized successfully on {app.config.get("SQLALCHEMY_DATABASE_URI", "unknown DB")}')
    
    return app
