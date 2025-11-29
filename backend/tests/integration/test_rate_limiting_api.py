"""
API Integration Tests for Email Verification Rate Limiting

Tests rate limiting at the API endpoint level.
"""
import pytest
from unittest.mock import patch
from flask import json
from app.repositories.implementations.user_repository import UserRepository


@pytest.mark.integration
@pytest.mark.api
class TestRateLimitingAPI:
    """Integration tests for rate limiting at API level."""

    # ============================================================================
    # Tests for POST /auth/register with Rate Limiting
    # ============================================================================

    @patch('app.services.auth.registration_service.NotificationService')
    def test_register_returns_429_when_rate_limit_exceeded(
        self,
        mock_notification,
        client,
        rotation_city
    ):
        """Test that registration returns 429 when rate limit is exceeded."""
        email = 'ratelimit@example.com'
        
        # Make 3 successful requests (at the limit)
        for i in range(3):
            response = client.post(
                '/api/v1/auth/register',
                json={
                    'email': email,
                    'first_name': 'Test',
                    'last_name': 'User',
                    'city_id': rotation_city.city_id
                },
                content_type='application/json'
            )
            assert response.status_code in [200, 201]
        
        # 4th request should be rate limited
        response = client.post(
            '/api/v1/auth/register',
            json={
                'email': email,
                'first_name': 'Test',
                'last_name': 'User',
                'city_id': rotation_city.city_id
            },
            content_type='application/json'
        )
        
        assert response.status_code == 429
        data = json.loads(response.data)
        assert 'Too many verification code requests' in data['message']

    @patch('app.services.auth.registration_service.NotificationService')
    def test_resend_code_returns_429_when_rate_limit_exceeded(
        self,
        mock_notification,
        client,
        rotation_city
    ):
        """Test that resend verification code returns 429 when rate limited."""
        email = 'resend@example.com'
        
        # Initial registration
        client.post(
            '/api/v1/auth/register',
            json={
                'email': email,
                'first_name': 'Test',
                'last_name': 'User',
                'city_id': rotation_city.city_id
            },
            content_type='application/json'
        )
        
        # Make 2 successful resend requests
        for i in range(2):
            response = client.post(
                '/api/v1/auth/register/resend-code',
                json={'email': email},
                content_type='application/json'
            )
            assert response.status_code == 200
        
        # 3rd resend should be rate limited (total 4 codes sent)
        response = client.post(
            '/api/v1/auth/register/resend-code',
            json={'email': email},
            content_type='application/json'
        )
        
        assert response.status_code == 429
        data = json.loads(response.data)
        assert 'Too many verification code requests' in data['message']

    @patch('app.services.auth.registration_service.NotificationService')
    def test_different_users_have_independent_rate_limits(
        self,
        mock_notification,
        client,
        rotation_city
    ):
        """Test that different users have independent rate limits."""
        # User 1 makes maximum requests
        for i in range(3):
            client.post(
                '/api/v1/auth/register',
                json={
                    'email': 'user1@example.com',
                    'first_name': 'User',
                    'last_name': 'One',
                    'city_id': rotation_city.city_id
                },
                content_type='application/json'
            )
        
        # User 1's next request should fail
        response1 = client.post(
            '/api/v1/auth/register',
            json={
                'email': 'user1@example.com',
                'first_name': 'User',
                'last_name': 'One',
                'city_id': rotation_city.city_id
            },
            content_type='application/json'
        )
        assert response1.status_code == 429
        
        # User 2 should still be able to register
        response2 = client.post(
            '/api/v1/auth/register',
            json={
                'email': 'user2@example.com',
                'first_name': 'User',
                'last_name': 'Two',
                'city_id': rotation_city.city_id
            },
            content_type='application/json'
        )
        assert response2.status_code == 201

    @patch('app.services.auth.registration_service.NotificationService')
    def test_rate_limit_error_message_includes_wait_time(
        self,
        mock_notification,
        client,
        rotation_city
    ):
        """Test that rate limit error message tells user how long to wait."""
        email = 'wait@example.com'
        
        # Exceed rate limit
        for i in range(4):
            client.post(
                '/api/v1/auth/register',
                json={
                    'email': email,
                    'first_name': 'Test',
                    'last_name': 'User',
                    'city_id': rotation_city.city_id
                },
                content_type='application/json'
            )
        
        # Check error message
        response = client.post(
            '/api/v1/auth/register',
            json={
                'email': email,
                'first_name': 'Test',
                'last_name': 'User',
                'city_id': rotation_city.city_id
            },
            content_type='application/json'
        )
        
        assert response.status_code == 429
        data = json.loads(response.data)
        assert 'wait' in data['message'].lower()
        assert 'minutes' in data['message'].lower()
