"""
Integration tests for category routes
"""
import pytest


class TestCategoryRoutes:
    """Test suite for /api/v1/categories endpoints"""

    def test_get_categories_success(self, client, category, furniture_category):
        """Test GET /api/v1/categories/ returns all categories"""
        response = client.get('/api/v1/categories/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert 'Electronics' in data
        assert 'Furniture' in data

    def test_get_categories_empty(self, client):
        """Test GET /api/v1/categories/ with no categories"""
        response = client.get('/api/v1/categories/')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
