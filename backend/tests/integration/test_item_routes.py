"""Integration tests for Item API endpoints."""
import pytest
from flask import json
from app.repositories.implementations.tag_repository import TagRepository
from app.repositories.implementations.category_repository import CategoryRepository
from app.models.category import Category
from app.services.auth.token_service import TokenService
from app import db


@pytest.mark.integration
@pytest.mark.api
class TestItemRoutes:
    """Test Item API endpoints."""

    def test_create_item_requires_authentication(self, client):
        """Test that POST /api/v1/item/ requires JWT token."""
        response = client.post('/api/v1/item/', json={})
        
        assert response.status_code == 401

    def test_create_item_requires_request_body(self, client, verified_user, app_context):
        """Test that request body is required."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {
            'Authorization': f'Bearer {tokens["access_token"]}'
        }
        
        response = client.post('/api/v1/item/', headers=headers, json={})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'message' in data or 'errors' in data

    def test_create_item_validates_required_fields(self, client, verified_user, app_context):
        """Test that required fields are validated."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        invalid_data = {}
        
        response = client.post('/api/v1/item/', 
                              headers=headers,
                              json=invalid_data)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data or 'message' in data

    def test_create_item_requires_at_least_one_category(self, client, verified_user, app_context):
        """Test that at least one category is required."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        invalid_data = {
            "name": "Test Item",
            "location": "Test Location",
            "category_ids": []  # Empty list
        }
        
        response = client.post('/api/v1/item/',
                              headers=headers,
                              json=invalid_data)
        
        assert response.status_code == 400

    def test_create_item_with_existing_tags_success(self, client, verified_user, app_context, db_session):
        """Test creating item with existing tags."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        # Create category
        category = Category(category_name="Furniture")
        db.session.add(category)
        db.session.commit()
        
        # Create tags
        tag_repo = TagRepository()
        tag1 = tag_repo.create_tag(name="Condition", value_type="text")
        tag2 = tag_repo.create_tag(name="Available", value_type="boolean")
        
        item_data = {
            "name": "Test Desk",
            "location": "Building A, Room 101",
            "walking_distance": 150.0,
            "category_ids": [category.category_id],
            "existing_tags": [
                {"tag_id": tag1.tag_id, "value": "Excellent"},
                {"tag_id": tag2.tag_id, "value": True}
            ],
            "new_tags": []
        }
        
        response = client.post('/api/v1/item/',
                              headers=headers,
                              json=item_data)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        assert 'item_id' in data
        assert data['name'] == "Test Desk"
        assert data['location'] == "Building A, Room 101"
        assert data['walking_distance'] == 150.0

    def test_create_item_with_new_tags_success(self, client, verified_user, app_context, db_session):
        """Test creating item with new tags."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        # Create category
        category = Category(category_name="Equipment")
        db.session.add(category)
        db.session.commit()
        
        item_data = {
            "name": "Projector",
            "location": "Conference Room B",
            "category_ids": [category.category_id],
            "existing_tags": [],
            "new_tags": [
                {
                    "name": "Brand",
                    "value_type": "text",
                    "value": "Epson"
                },
                {
                    "name": "Working",
                    "value_type": "boolean",
                    "value": True
                }
            ]
        }
        
        response = client.post('/api/v1/item/',
                              headers=headers,
                              json=item_data)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        assert data['name'] == "Projector"
        assert data['location'] == "Conference Room B"

    def test_create_item_with_mixed_tags_success(self, client, verified_user, app_context, db_session):
        """Test creating item with both existing and new tags."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        # Create category
        category = Category(category_name="Tools")
        db.session.add(category)
        db.session.commit()
        
        # Create existing tag
        tag_repo = TagRepository()
        existing_tag = tag_repo.create_tag(name="Color", value_type="text")
        
        item_data = {
            "name": "Hammer",
            "location": "Workshop",
            "category_ids": [category.category_id],
            "existing_tags": [
                {"tag_id": existing_tag.tag_id, "value": "Red"}
            ],
            "new_tags": [
                {
                    "name": "Weight",
                    "value_type": "numeric",
                    "value": 2.5
                }
            ]
        }
        
        response = client.post('/api/v1/item/',
                              headers=headers,
                              json=item_data)
        
        assert response.status_code == 201

    def test_create_item_rejects_invalid_category(self, client, verified_user, app_context):
        """Test that invalid category ID is rejected."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        item_data = {
            "name": "Test Item",
            "location": "Test Location",
            "category_ids": [99999],  # Non-existent category
            "existing_tags": [],
            "new_tags": []
        }
        
        response = client.post('/api/v1/item/',
                              headers=headers,
                              json=item_data)
        
        assert response.status_code == 400

    def test_create_item_rejects_duplicate_categories(self, client, verified_user, app_context, db_session):
        """Test that duplicate category IDs are rejected."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        category = Category(category_name="Test")
        db.session.add(category)
        db.session.commit()
        
        item_data = {
            "name": "Test Item",
            "location": "Test Location",
            "category_ids": [category.category_id, category.category_id],  # Duplicate
            "existing_tags": [],
            "new_tags": []
        }
        
        response = client.post('/api/v1/item/',
                              headers=headers,
                              json=item_data)
        
        assert response.status_code == 400

    def test_create_item_validates_new_tag_value_type(self, client, verified_user, app_context, db_session):
        """Test that new tag value_type is validated."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        category = Category(category_name="Test")
        db.session.add(category)
        db.session.commit()
        
        item_data = {
            "name": "Test Item",
            "location": "Test Location",
            "category_ids": [category.category_id],
            "existing_tags": [],
            "new_tags": [
                {
                    "name": "Invalid",
                    "value_type": "invalid_type",  # Invalid type
                    "value": "test"
                }
            ]
        }
        
        response = client.post('/api/v1/item/',
                              headers=headers,
                              json=item_data)
        
        assert response.status_code == 400

    def test_create_item_without_walking_distance(self, client, verified_user, app_context, db_session):
        """Test creating item without walking distance (optional field)."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        category = Category(category_name="Test")
        db.session.add(category)
        db.session.commit()
        
        item_data = {
            "name": "Test Item",
            "location": "Test Location",
            "category_ids": [category.category_id],
            "existing_tags": [],
            "new_tags": []
        }
        
        response = client.post('/api/v1/item/',
                              headers=headers,
                              json=item_data)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['walking_distance'] is None

    def test_create_item_rejects_empty_name(self, client, verified_user, app_context, db_session):
        """Test that empty name is rejected."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        category = Category(category_name="Test")
        db.session.add(category)
        db.session.commit()
        
        item_data = {
            "name": "   ",  # Only whitespace
            "location": "Test Location",
            "category_ids": [category.category_id],
            "existing_tags": [],
            "new_tags": []
        }
        
        response = client.post('/api/v1/item/',
                              headers=headers,
                              json=item_data)
        
        assert response.status_code == 400

    def test_create_item_rejects_negative_walking_distance(self, client, verified_user, app_context, db_session):
        """Test that negative walking distance is rejected."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        category = Category(category_name="Test")
        db.session.add(category)
        db.session.commit()
        
        item_data = {
            "name": "Test Item",
            "location": "Test Location",
            "walking_distance": -10.0,  # Negative
            "category_ids": [category.category_id],
            "existing_tags": [],
            "new_tags": []
        }
        
        response = client.post('/api/v1/item/',
                              headers=headers,
                              json=item_data)
        
        assert response.status_code == 400

    def test_get_all_items_requires_authentication(self, client):
        """Test that GET /api/v1/item/ requires JWT token."""
        response = client.get('/api/v1/item/')
        
        assert response.status_code == 401

    def test_get_all_items_empty(self, client, verified_user, app_context):
        """Test getting all items when none exist."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        response = client.get('/api/v1/item/', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_get_all_items_returns_list(self, client, verified_user, app_context, db_session):
        """Test getting all items returns proper list."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        # Create categories
        category1 = Category(category_name="Electronics")
        category2 = Category(category_name="Furniture")
        db.session.add_all([category1, category2])
        db.session.commit()
        
        # Create items via the API
        item1_data = {
            "name": "Laptop",
            "location": "Office A",
            "category_ids": [category1.category_id],
            "existing_tags": [],
            "new_tags": []
        }
        
        item2_data = {
            "name": "Desk",
            "location": "Office B",
            "walking_distance": 100.0,
            "category_ids": [category2.category_id],
            "existing_tags": [],
            "new_tags": []
        }
        
        client.post('/api/v1/item/', headers=headers, json=item1_data)
        client.post('/api/v1/item/', headers=headers, json=item2_data)
        
        # Get all items
        response = client.get('/api/v1/item/', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert all('item_id' in item for item in data)
        assert all('name' in item for item in data)
        assert all('location' in item for item in data)

    def test_get_item_by_id_requires_authentication(self, client):
        """Test that GET /api/v1/item/<id> requires JWT token."""
        response = client.get('/api/v1/item/1')
        
        assert response.status_code == 401

    def test_get_item_by_id_success(self, client, verified_user, app_context, db_session):
        """Test getting item by ID when it exists."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        # Create category and item
        category = Category(category_name="Books")
        db.session.add(category)
        db.session.commit()
        
        item_data = {
            "name": "Python Programming",
            "location": "Library, Shelf 3",
            "walking_distance": 200.0,
            "category_ids": [category.category_id],
            "existing_tags": [],
            "new_tags": []
        }
        
        # Create item
        create_response = client.post('/api/v1/item/', headers=headers, json=item_data)
        created_item = json.loads(create_response.data)
        item_id = created_item['item_id']
        
        # Get item by ID
        response = client.get(f'/api/v1/item/{item_id}', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['item_id'] == item_id
        assert data['name'] == "Python Programming"
        assert data['location'] == "Library, Shelf 3"
        assert data['walking_distance'] == 200.0

    def test_get_item_by_id_not_found(self, client, verified_user, app_context):
        """Test getting item by ID when it doesn't exist."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        response = client.get('/api/v1/item/99999', headers=headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'message' in data
        assert 'not found' in data['message'].lower()

    def test_get_user_items_requires_authentication(self, client):
        """Test that GET /api/v1/item/user/<user_id> requires JWT token."""
        response = client.get('/api/v1/item/user/1')
        
        assert response.status_code == 401

    def test_get_user_items_empty_list(self, client, verified_user, app_context):
        """Test getting user items when user has no items."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        response = client.get(f'/api/v1/item/user/{verified_user.user_id}', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
        assert isinstance(data, list)

    def test_get_user_items_returns_only_user_items(self, client, verified_user, second_user, app_context, db_session):
        """Test that endpoint returns only items added by the specified user."""
        # Create tokens for both users
        user1_tokens = TokenService.generate_tokens(verified_user)
        user2_tokens = TokenService.generate_tokens(second_user)
        user1_headers = {'Authorization': f'Bearer {user1_tokens["access_token"]}'}
        user2_headers = {'Authorization': f'Bearer {user2_tokens["access_token"]}'}
        
        # Create category
        category = Category(category_name="TestCategory")
        db.session.add(category)
        db.session.commit()
        
        # User 1 creates 2 items
        item1_data = {
            "name": "User1 Item1",
            "location": "Location A",
            "category_ids": [category.category_id],
            "existing_tags": [],
            "new_tags": []
        }
        item2_data = {
            "name": "User1 Item2",
            "location": "Location B",
            "category_ids": [category.category_id],
            "existing_tags": [],
            "new_tags": []
        }
        
        client.post('/api/v1/item/', headers=user1_headers, json=item1_data)
        client.post('/api/v1/item/', headers=user1_headers, json=item2_data)
        
        # User 2 creates 1 item
        item3_data = {
            "name": "User2 Item1",
            "location": "Location C",
            "category_ids": [category.category_id],
            "existing_tags": [],
            "new_tags": []
        }
        
        client.post('/api/v1/item/', headers=user2_headers, json=item3_data)
        
        # Get user1's items
        response = client.get(f'/api/v1/item/user/{verified_user.user_id}', headers=user1_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert all(item['name'].startswith('User1') for item in data)
        
        # Get user2's items
        response = client.get(f'/api/v1/item/user/{second_user.user_id}', headers=user2_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['name'] == "User2 Item1"

    def test_get_user_items_includes_full_details(self, client, verified_user, app_context, db_session):
        """Test that user items include categories, tags, and all details."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        # Create category
        category = Category(category_name="Electronics")
        db.session.add(category)
        db.session.commit()
        
        # Create item with new tag
        item_data = {
            "name": "Laptop",
            "location": "Office 101",
            "walking_distance": 50.0,
            "category_ids": [category.category_id],
            "existing_tags": [],
            "new_tags": [
                {
                    "name": "Brand",
                    "value_type": "text",
                    "value": "Dell"
                }
            ]
        }
        
        client.post('/api/v1/item/', headers=headers, json=item_data)
        
        # Get user items
        response = client.get(f'/api/v1/item/user/{verified_user.user_id}', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        
        item = data[0]
        assert item['name'] == "Laptop"
        assert item['location'] == "Office 101"
        assert item['walking_distance'] == 50.0
        assert 'categories' in item
        assert len(item['categories']) == 1
        assert item['categories'][0]['category_name'] == "Electronics"
        assert 'tags' in item
        assert len(item['tags']) == 1
        assert item['tags'][0]['name'] == "Brand"
        assert item['tags'][0]['value'] == "Dell"

    def test_get_user_items_nonexistent_user(self, client, verified_user, app_context):
        """Test getting items for non-existent user returns 404."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        response = client.get('/api/v1/item/user/99999', headers=headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'message' in data
        assert 'not found' in data['message'].lower()

    def test_get_user_items_ordered_by_newest_first(self, client, verified_user, app_context, db_session):
        """Test that user items are ordered by creation date (newest first)."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        # Create category
        category = Category(category_name="Test")
        db.session.add(category)
        db.session.commit()
        
        # Create 3 items
        for i in range(3):
            item_data = {
                "name": f"Item {i}",
                "location": f"Location {i}",
                "category_ids": [category.category_id],
                "existing_tags": [],
                "new_tags": []
            }
            client.post('/api/v1/item/', headers=headers, json=item_data)
        
        # Get user items
        response = client.get(f'/api/v1/item/user/{verified_user.user_id}', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 3
        # Newest should be first (Item 2, Item 1, Item 0)
        assert data[0]['name'] == "Item 2"
        assert data[1]['name'] == "Item 1"
        assert data[2]['name'] == "Item 0"

