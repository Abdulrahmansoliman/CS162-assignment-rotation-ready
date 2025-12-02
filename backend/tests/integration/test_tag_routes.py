"""Integration tests for Tag API endpoints."""
import pytest
from flask import json
from app.repositories.implementations.tag_repository import TagRepository
from app.services.auth.token_service import TokenService


@pytest.mark.integration
@pytest.mark.api
class TestTagRoutes:
    """Test Tag API endpoints."""

    def test_get_all_tags_requires_authentication(self, client):
        """Test that GET /api/v1/tag/ requires JWT token."""
        response = client.get('/api/v1/tag/')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'message' in data or 'msg' in data

    def test_get_all_tags_empty(self, client, verified_user, app_context):
        """Test getting all tags when database is empty."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        response = client.get('/api/v1/tag/', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_all_tags_returns_correct_structure(self, client, verified_user, app_context, db_session):
        """Test that tags are returned with correct structure."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        # Create some test tags
        tag_repo = TagRepository()
        tag_repo.create_tag(name="Condition", value_type="text")
        tag_repo.create_tag(name="Available", value_type="boolean")
        tag_repo.create_tag(name="Price", value_type="numeric")
        
        response = client.get('/api/v1/tag/', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Check structure of each tag
        for tag in data:
            assert 'tag_id' in tag
            assert 'name' in tag
            assert 'value_type' in tag
            assert isinstance(tag['tag_id'], int)
            assert isinstance(tag['name'], str)
            assert tag['value_type'] in ['text', 'boolean', 'numeric']

    def test_get_all_tags_ordered_alphabetically(self, client, verified_user, app_context, db_session):
        """Test that tags are returned in alphabetical order."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        tag_repo = TagRepository()
        tag_repo.create_tag(name="Zebra", value_type="text")
        tag_repo.create_tag(name="Apple", value_type="boolean")
        tag_repo.create_tag(name="Mango", value_type="numeric")
        
        response = client.get('/api/v1/tag/', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data[0]['name'] == "Apple"
        assert data[1]['name'] == "Mango"
        assert data[2]['name'] == "Zebra"

    def test_get_all_tags_includes_all_value_types(self, client, verified_user, app_context, db_session):
        """Test that different value types are returned correctly."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        tag_repo = TagRepository()
        tag_repo.create_tag(name="Material", value_type="text")
        tag_repo.create_tag(name="InStock", value_type="boolean")
        tag_repo.create_tag(name="Weight", value_type="numeric")
        
        response = client.get('/api/v1/tag/', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        value_types = [tag['value_type'] for tag in data]
        assert 'text' in value_types
        assert 'boolean' in value_types
        assert 'numeric' in value_types

    def test_get_all_tags_multiple_requests_consistent(self, client, verified_user, app_context, db_session):
        """Test that multiple requests return consistent data."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        tag_repo = TagRepository()
        tag_repo.create_tag(name="Test1", value_type="text")
        tag_repo.create_tag(name="Test2", value_type="boolean")
        
        response1 = client.get('/api/v1/tag/', headers=headers)
        response2 = client.get('/api/v1/tag/', headers=headers)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        
        assert data1 == data2
