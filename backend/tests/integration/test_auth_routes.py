"""Integration tests for authentication routes."""
import pytest

from app.services.auth.token_service import TokenService


@pytest.mark.integration
class TestAuthRefreshRoute:
    """Tests for the /api/v1/auth/refresh endpoint."""

    def test_refresh_returns_new_access_token(
        self,
        client,
        verified_user,
        app_context
    ):
        tokens = TokenService.generate_tokens(verified_user)
        refresh_token = tokens['refresh_token']

        response = client.post(
            '/api/v1/auth/refresh',
            headers={'Authorization': f'Bearer {refresh_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert isinstance(data['access_token'], str)
        assert data['access_token']

    def test_refresh_requires_refresh_token(self, client):
        response = client.post('/api/v1/auth/refresh')

        assert response.status_code == 401

    def test_refresh_returns_404_when_user_missing(
        self,
        client,
        verified_user,
        db_session,
        app_context
    ):
        tokens = TokenService.generate_tokens(verified_user)
        refresh_token = tokens['refresh_token']

        db_user = db_session.get(type(verified_user), verified_user.user_id)
        db_session.delete(db_user)
        db_session.commit()

        response = client.post(
            '/api/v1/auth/refresh',
            headers={'Authorization': f'Bearer {refresh_token}'}
        )

        assert response.status_code == 404
        data = response.get_json()
        assert data['message'] == 'User not found.'
