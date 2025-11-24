"""
Integration Tests for TokenService

Tests JWT token generation and validation.
"""
import pytest
from flask_jwt_extended import decode_token
from app.services.auth.token_service import TokenService
from flask import current_app


@pytest.mark.integration
@pytest.mark.service
class TestTokenService:
    """Tests for JWT token generation."""

    def test_generate_tokens_creates_access_and_refresh(self, verified_user):
        tokens = TokenService.generate_tokens(verified_user)
        
        assert 'access_token' in tokens
        assert 'refresh_token' in tokens
        assert isinstance(tokens['access_token'], str)
        assert isinstance(tokens['refresh_token'], str)

    def test_access_token_contains_user_claims(self, verified_user, app_context):
        tokens = TokenService.generate_tokens(verified_user)
        
        decoded = decode_token(tokens['access_token'])
        assert decoded['sub'] == str(verified_user.user_id)
        assert decoded['email'] == verified_user.email
        assert decoded['first_name'] == verified_user.first_name
        assert decoded['last_name'] == verified_user.last_name

    def test_refresh_token_contains_user_id(self, verified_user, app_context):
        tokens = TokenService.generate_tokens(verified_user)
        
        decoded = decode_token(tokens['refresh_token'])
        assert decoded['sub'] == str(verified_user.user_id)

    def test_generate_access_token_from_user(self, verified_user, app_context):
        token = TokenService.generate_access_token(verified_user)
        
        decoded = decode_token(token)
        assert decoded['sub'] == str(verified_user.user_id)
        assert decoded['email'] == verified_user.email

    def test_access_token_has_expiry(self, verified_user, app_context):
        tokens = TokenService.generate_tokens(verified_user)
        
        decoded = decode_token(tokens['access_token'])
        assert 'exp' in decoded
        
        access_expiry = decoded['exp']
        issued_at = decoded['iat']
        token_lifetime = access_expiry - issued_at
        
        expected_lifetime = current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        if hasattr(expected_lifetime, 'total_seconds'):
            expected_lifetime = int(expected_lifetime.total_seconds())
        
        assert token_lifetime == expected_lifetime

    def test_tokens_are_different(self, verified_user):
        tokens = TokenService.generate_tokens(verified_user)
        
        assert tokens['access_token'] != tokens['refresh_token']
