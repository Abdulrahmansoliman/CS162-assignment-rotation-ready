"""
Integration tests for item routes
"""
import pytest


class TestItemRoutes:
    """Test suite for /api/v1/items endpoints"""

    def test_get_item_success(self, client, item):
        """Test GET /api/v1/items/<id> returns item data"""
        response = client.get(f'/api/v1/items/{item.item_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['item_id'] == item.item_id
        assert data['name'] == 'Laptop'
        assert data['location'] == 'Library Floor 2'
        assert data['walking_distance'] == 150.5

    def test_get_item_not_found(self, client):
        """Test GET /api/v1/items/<id> with non-existent item"""
        response = client.get('/api/v1/items/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_get_all_items(self, client, item, book):
        """Test GET /api/v1/items/ returns all items"""
        response = client.get('/api/v1/items/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert 'Laptop' in data
        assert 'Introduction to Algorithms' in data

    def test_get_all_items_empty(self, client):
        """Test GET /api/v1/items/ with no items"""
        response = client.get('/api/v1/items/')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_create_item_success(self, client, user):
        """Test POST /api/v1/items creates new item"""
        item_data = {
            'name': 'New Laptop',
            'location': 'Dorm Room',
            'added_by_user_id': user.user_id,
            'walking_distance': 50.0
        }
        
        response = client.post('/api/v1/items/', json=item_data)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'New Laptop'
        assert data['location'] == 'Dorm Room'
        assert data['walking_distance'] == 50.0
        assert data['added_by_user_id'] == user.user_id

    def test_create_item_missing_required_fields(self, client):
        """Test POST /api/v1/items with missing required fields"""
        item_data = {
            'name': 'Incomplete Item'
            # Missing location and added_by_user_id
        }
        
        response = client.post('/api/v1/items/', json=item_data)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Missing' in data['error']

    def test_create_item_no_body(self, client):
        """Test POST /api/v1/items with empty JSON object"""
        response = client.post('/api/v1/items/', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_create_item_optional_walking_distance(self, client, user):
        """Test POST /api/v1/items without optional walking_distance"""
        item_data = {
            'name': 'Chair',
            'location': 'Study Room',
            'added_by_user_id': user.user_id
        }
        
        response = client.post('/api/v1/items/', json=item_data)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'Chair'
