"""
Integration tests for rotation city routes
"""
import pytest


class TestRotationCityRoutes:
    """Test suite for /api/v1/rotation-city endpoints"""

    def test_get_rotation_cities_success(self, client, rotation_city):
        """Test GET /api/v1/rotation-city/ returns cities"""
        response = client.get('/api/v1/rotation-city/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert 'San Francisco' in data

    def test_get_rotation_cities_empty(self, client):
        """Test GET /api/v1/rotation-city/ with no cities"""
        response = client.get('/api/v1/rotation-city/')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
