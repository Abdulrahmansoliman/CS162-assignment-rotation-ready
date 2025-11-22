"""
Integration tests for user routes
"""
import pytest


class TestUserRoutes:
    """Test suite for /api/v1/user endpoints"""

    def test_get_user_success(self, client, user):
        """Test GET /api/v1/user/<id> returns user data"""
        response = client.get(f'/api/v1/user/{user.user_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['user_id'] == user.user_id
        assert data['email'] == 'john@example.com'
        assert data['first_name'] == 'John'
        assert data['last_name'] == 'Doe'

    def test_get_user_not_found(self, client):
        """Test GET /api/v1/user/<id> with non-existent user"""
        response = client.get('/api/v1/user/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'User not found'

    def test_get_verified_user(self, client, verified_user):
        """Test GET /api/v1/user/<id> for verified user"""
        response = client.get(f'/api/v1/user/{verified_user.user_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == 'bob@example.com'
