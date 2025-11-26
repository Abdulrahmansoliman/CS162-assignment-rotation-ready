"""
Integration Tests for Password Reset API Routes

Tests the password reset API endpoints with real HTTP requests.
Uses real database and validates complete request/response flow.
"""
import pytest
from unittest.mock import patch
from flask import json
from app.models.user import User
from app.models.verification_code import VerificationCode, VerificationCodeType
from app.repositories.implementations.user_repository import UserRepository
from datetime import datetime, timedelta
from app import db


@pytest.mark.integration
@pytest.mark.api
class TestPasswordResetAPIIntegration:
    """Integration tests for password reset API routes."""

    @pytest.fixture
    def verified_user(self, rotation_city, db_session):
        """Create a verified user with password."""
        user_repo = UserRepository()
        user = user_repo.create_user(
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            rotation_city_id=rotation_city.city_id
        )
        user.set_password('oldpassword123')
        user.is_verified = True
        db_session.commit()
        db_session.refresh(user)
        return user

    # ============================================================================
    # Tests for POST /auth/password-reset/request
    # ============================================================================

    @patch('app.services.auth.password_reset_service.NotificationService')
    def test_request_password_reset_returns_202_for_valid_email(
        self,
        mock_notification,
        client,
        verified_user
    ):
        """Test that password reset request returns 202 for valid email."""
        response = client.post(
            '/api/v1/auth/password-reset/request',
            json={'email': 'testuser@example.com'},
            content_type='application/json'
        )
        
        assert response.status_code == 202
        data = json.loads(response.data)
        assert 'message' in data
        assert 'reset link has been sent' in data['message'].lower()

    @patch('app.services.auth.password_reset_service.NotificationService')
    def test_request_password_reset_returns_202_for_nonexistent_email(
        self,
        mock_notification,
        client
    ):
        """Test that password reset request returns 202 even for non-existent email."""
        response = client.post(
            '/api/v1/auth/password-reset/request',
            json={'email': 'nonexistent@example.com'},
            content_type='application/json'
        )
        
        # Should return success to prevent email enumeration
        assert response.status_code == 202
        data = json.loads(response.data)
        assert 'message' in data

    def test_request_password_reset_returns_400_for_missing_email(
        self,
        client
    ):
        """Test that password reset request returns 400 when email is missing."""
        response = client.post(
            '/api/v1/auth/password-reset/request',
            json={},
            content_type='application/json'
        )
        
        assert response.status_code == 400

    @patch('app.services.auth.password_reset_service.NotificationService')
    def test_request_password_reset_creates_verification_code(
        self,
        mock_notification,
        client,
        verified_user,
        db_session
    ):
        """Test that password reset request creates a verification code."""
        response = client.post(
            '/api/v1/auth/password-reset/request',
            json={'email': 'testuser@example.com'},
            content_type='application/json'
        )
        
        assert response.status_code == 202
        
        # Check that verification code was created
        code = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.PASSWORD_RESET.code,
            is_used=False
        ).first()
        
        assert code is not None

    # ============================================================================
    # Tests for POST /auth/password-reset/verify
    # ============================================================================

    @patch('app.services.auth.password_reset_service.NotificationService')
    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_verify_password_reset_returns_200_for_valid_token(
        self,
        mock_token,
        mock_notification,
        client,
        verified_user,
        app_context
    ):
        """Test that password reset verify returns 200 for valid token."""
        mock_token.return_value = 'valid_reset_token'
        
        # Request reset
        client.post(
            '/api/v1/auth/password-reset/request',
            json={'email': 'testuser@example.com'},
            content_type='application/json'
        )
        
        # Verify reset
        response = client.post(
            '/api/v1/auth/password-reset/verify',
            json={
                'token': 'valid_reset_token',
                'new_password': 'newstrongpassword123'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'Password updated successfully' in data['message']

    def test_verify_password_reset_returns_400_for_invalid_token(
        self,
        client,
        verified_user
    ):
        """Test that password reset verify returns 400 for invalid token."""
        response = client.post(
            '/api/v1/auth/password-reset/verify',
            json={
                'token': 'invalid_token',
                'new_password': 'newpassword123'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Invalid or expired' in data['message']

    def test_verify_password_reset_returns_400_for_missing_token(
        self,
        client
    ):
        """Test that password reset verify returns 400 when token is missing."""
        response = client.post(
            '/api/v1/auth/password-reset/verify',
            json={'new_password': 'newpassword123'},
            content_type='application/json'
        )
        
        assert response.status_code == 400

    def test_verify_password_reset_returns_400_for_missing_password(
        self,
        client
    ):
        """Test that password reset verify returns 400 when password is missing."""
        response = client.post(
            '/api/v1/auth/password-reset/verify',
            json={'token': 'some_token'},
            content_type='application/json'
        )
        
        assert response.status_code == 400

    def test_verify_password_reset_returns_400_for_short_password(
        self,
        client
    ):
        """Test that password reset verify returns 400 for password too short."""
        response = client.post(
            '/api/v1/auth/password-reset/verify',
            json={
                'token': 'some_token',
                'new_password': 'short'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'at least 8 characters' in data['message']

    @patch('app.services.auth.password_reset_service.NotificationService')
    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_verify_password_reset_actually_updates_password(
        self,
        mock_token,
        mock_notification,
        client,
        verified_user,
        db_session
    ):
        """Test that password reset verify actually updates the user's password."""
        mock_token.return_value = 'valid_reset_token'
        
        # Request reset
        client.post(
            '/api/v1/auth/password-reset/request',
            json={'email': 'testuser@example.com'},
            content_type='application/json'
        )
        
        # Verify reset
        client.post(
            '/api/v1/auth/password-reset/verify',
            json={
                'token': 'valid_reset_token',
                'new_password': 'mynewpassword123'
            },
            content_type='application/json'
        )
        
        # Check password was actually updated
        db_session.refresh(verified_user)
        assert verified_user.check_password('mynewpassword123') is True
        assert verified_user.check_password('oldpassword123') is False

    @patch('app.services.auth.password_reset_service.NotificationService')
    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_verify_password_reset_token_can_only_be_used_once(
        self,
        mock_token,
        mock_notification,
        client,
        verified_user
    ):
        """Test that reset token can only be used once."""
        mock_token.return_value = 'one_time_token'
        
        # Request reset
        client.post(
            '/api/v1/auth/password-reset/request',
            json={'email': 'testuser@example.com'},
            content_type='application/json'
        )
        
        # First verification should succeed
        response1 = client.post(
            '/api/v1/auth/password-reset/verify',
            json={
                'token': 'one_time_token',
                'new_password': 'newpassword123'
            },
            content_type='application/json'
        )
        assert response1.status_code == 200
        
        # Second verification with same token should fail
        response2 = client.post(
            '/api/v1/auth/password-reset/verify',
            json={
                'token': 'one_time_token',
                'new_password': 'anotherpassword'
            },
            content_type='application/json'
        )
        assert response2.status_code == 400

    # ============================================================================
    # Tests for Complete Password Reset Flow via API
    # ============================================================================

    @patch('app.services.auth.password_reset_service.NotificationService')
    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_complete_password_reset_flow_via_api(
        self,
        mock_token,
        mock_notification,
        client,
        verified_user,
        db_session
    ):
        """Test complete password reset flow through API endpoints."""
        mock_token.return_value = 'complete_flow_token'
        
        # Step 1: Request password reset
        response1 = client.post(
            '/api/v1/auth/password-reset/request',
            json={'email': 'testuser@example.com'},
            content_type='application/json'
        )
        assert response1.status_code == 202
        
        # Verify code was created
        code = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.PASSWORD_RESET.code,
            is_used=False
        ).first()
        assert code is not None
        
        # Step 2: Verify and reset password
        response2 = client.post(
            '/api/v1/auth/password-reset/verify',
            json={
                'token': 'complete_flow_token',
                'new_password': 'completelynewpassword123'
            },
            content_type='application/json'
        )
        assert response2.status_code == 200
        
        # Verify password was updated
        db_session.refresh(verified_user)
        assert verified_user.check_password('completelynewpassword123') is True
        
        # Verify code was marked as used
        db_session.refresh(code)
        assert code.is_used is True
