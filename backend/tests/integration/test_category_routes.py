"""
Integration tests for category routes
"""
import pytest
from app.services.auth.token_service import TokenService


@pytest.mark.integration
class TestCategoryRoutes:
    """Test suite for /api/v1/category endpoints"""

    def test_get_all_categories_success(
        self, client, category, verified_user, app_context
    ):
        """Test GET /api/v1/category/ returns all categories with JWT"""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            '/api/v1/category/',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Verify response structure includes images by default
        cat = data[0]
        assert 'category_id' in cat
        assert 'category_name' in cat
        assert 'category_pic' in cat
        assert cat['category_name'] == 'Electronics'

    def test_get_all_categories_no_images(
        self, client, category, verified_user, app_context
    ):
        """Test GET /api/v1/category/?no_images=true excludes pictures"""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            '/api/v1/category/?no_images=true',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Verify response excludes category_pic
        cat = data[0]
        assert 'category_id' in cat
        assert 'category_name' in cat
        assert 'category_pic' not in cat

    def test_get_all_categories_requires_auth(self, client, category):
        """Test GET /api/v1/category/ requires JWT authentication"""
        response = client.get('/api/v1/category/')
        
        assert response.status_code == 401

    def test_get_all_categories_empty(
        self, client, verified_user, app_context
    ):
        """Test GET /api/v1/category/ with no categories"""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            '/api/v1/category/',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_get_category_by_id_success(
        self, client, category, verified_user, app_context
    ):
        """Test GET /api/v1/category/<id> returns specific category"""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            f'/api/v1/category/{category.category_id}',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['category_id'] == category.category_id
        assert data['category_name'] == category.category_name
        assert data['category_pic'] == category.category_pic

    def test_get_category_by_id_no_images(
        self, client, category, verified_user, app_context
    ):
        """Test GET /api/v1/category/<id>?no_images=true excludes picture"""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            f'/api/v1/category/{category.category_id}?no_images=true',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['category_id'] == category.category_id
        assert data['category_name'] == category.category_name
        assert 'category_pic' not in data

    def test_get_category_by_id_not_found(
        self, client, verified_user, app_context
    ):
        """Test GET /api/v1/category/<id> with non-existent ID"""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            '/api/v1/category/99999',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Category not found'

    def test_get_category_by_id_requires_auth(self, client, category):
        """Test GET /api/v1/category/<id> requires JWT authentication"""
        response = client.get(f'/api/v1/category/{category.category_id}')
        
        assert response.status_code == 401

    def test_get_multiple_categories(
        self,
        client,
        category,
        furniture_category,
        books_category,
        verified_user,
        app_context
    ):
        """Test GET /api/v1/category/ returns multiple categories"""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            '/api/v1/category/',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        
        # Verify all categories are present
        category_names = {cat['category_name'] for cat in data}
        assert 'Electronics' in category_names
        assert 'Furniture' in category_names
        assert 'Books' in category_names

    def test_get_categories_with_invalid_token(self, client, category):
        """Test GET /api/v1/category/ with invalid JWT token"""
        response = client.get(
            '/api/v1/category/',
            headers={'Authorization': 'Bearer invalid_token_here'}
        )
        
        assert response.status_code == 401
