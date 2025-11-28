"""
Integration tests for category routes
"""
import pytest
from app.models.category import Category


@pytest.mark.integration
class TestCategoryRoutes:
    """Test suite for /api/v1/category endpoints"""

    def test_get_all_categories_success(self, client, category):
        """Test GET /api/v1/category/ returns all categories"""
        # Act
        response = client.get('/api/v1/category/')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['category_name'] == category.category_name

    def test_get_all_categories_empty(self, client):
        """Test GET /api/v1/category/ returns 404 when no categories"""
        # Act
        response = client.get('/api/v1/category/')

        # Assert
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_get_category_by_id_success(self, client, category):
        """Test GET /api/v1/category/<id> returns specific category"""
        # Act
        response = client.get(f'/api/v1/category/{category.category_id}')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['category_id'] == category.category_id
        assert data['category_name'] == category.category_name

    def test_get_category_by_id_not_found(self, client):
        """Test GET /api/v1/category/<id> returns 404 when not found"""
        # Act
        response = client.get('/api/v1/category/999')

        # Assert
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_create_category_success(self, client, auth_headers):
        """Test POST /api/v1/category/ creates new category"""
        # Arrange
        category_data = {
            'category_name': 'Electronics',
            'category_pic': 'electronics.jpg'
        }

        # Act
        response = client.post(
            '/api/v1/category/',
            json=category_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 201
        data = response.get_json()
        assert data['category_name'] == 'Electronics'
        assert data['category_pic'] == 'electronics.jpg'
        assert 'category_id' in data

    def test_create_category_no_pic(self, client, auth_headers):
        """Test POST /api/v1/category/ works without picture"""
        # Arrange
        category_data = {
            'category_name': 'Books'
        }

        # Act
        response = client.post(
            '/api/v1/category/',
            json=category_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 201
        data = response.get_json()
        assert data['category_name'] == 'Books'
        assert data['category_pic'] is None

    def test_create_category_missing_name(self, client, auth_headers):
        """Test POST /api/v1/category/ returns 400 when name missing"""
        # Arrange
        category_data = {
            'category_pic': 'pic.jpg'
        }

        # Act
        response = client.post(
            '/api/v1/category/',
            json=category_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_create_category_no_auth(self, client):
        """Test POST /api/v1/category/ returns 401 without authentication"""
        # Arrange
        category_data = {
            'category_name': 'Electronics'
        }

        # Act
        response = client.post(
            '/api/v1/category/',
            json=category_data
        )

        # Assert
        assert response.status_code == 401

    def test_update_category_success(self, client, category, auth_headers):
        """Test PUT /api/v1/category/<id> updates category"""
        # Arrange
        update_data = {
            'category_name': 'Updated Name',
            'category_pic': 'updated.jpg'
        }

        # Act
        response = client.put(
            f'/api/v1/category/{category.category_id}',
            json=update_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['category_name'] == 'Updated Name'
        assert data['category_pic'] == 'updated.jpg'

    def test_update_category_partial(self, client, category, auth_headers):
        """Test PUT /api/v1/category/<id> allows partial update"""
        # Arrange
        update_data = {
            'category_name': 'Updated Name Only'
        }

        # Act
        response = client.put(
            f'/api/v1/category/{category.category_id}',
            json=update_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['category_name'] == 'Updated Name Only'

    def test_update_category_not_found(self, client, auth_headers):
        """Test PUT /api/v1/category/<id> returns 404 when not found"""
        # Arrange
        update_data = {
            'category_name': 'Updated Name'
        }

        # Act
        response = client.put(
            '/api/v1/category/999',
            json=update_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 404

    def test_update_category_no_auth(self, client, category):
        """Test PUT /api/v1/category/<id> returns 401 without authentication"""
        # Arrange
        update_data = {
            'category_name': 'Updated Name'
        }

        # Act
        response = client.put(
            f'/api/v1/category/{category.category_id}',
            json=update_data
        )

        # Assert
        assert response.status_code == 401

    def test_delete_category_success(self, client, category, auth_headers):
        """Test DELETE /api/v1/category/<id> deletes category"""
        # Act
        response = client.delete(
            f'/api/v1/category/{category.category_id}',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data or 'Category deleted successfully' in str(data)

    def test_delete_category_not_found(self, client, auth_headers):
        """Test DELETE /api/v1/category/<id> returns 404 when not found"""
        # Act
        response = client.delete(
            '/api/v1/category/999',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 404

    def test_delete_category_no_auth(self, client, category):
        """Test DELETE /api/v1/category/<id> returns 401 without authentication"""
        # Act
        response = client.delete(f'/api/v1/category/{category.category_id}')

        # Assert
        assert response.status_code == 401


if __name__ == '__main__':
    pytest.main([__file__, '-v'])