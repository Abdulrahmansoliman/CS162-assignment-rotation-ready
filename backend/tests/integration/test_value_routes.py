"""Integration tests for Value API endpoints."""
import pytest
from flask import json
from app.repositories.implementations.tag_repository import TagRepository
from app.repositories.implementations.value_repository import ValueRepository
from app.services.auth.token_service import TokenService


@pytest.mark.integration
@pytest.mark.api
class TestValueRoutes:
    """Test Value API endpoints."""

    def test_get_text_values_by_tag(self, client, verified_user, app_context, db_session):
        """Test getting text values for a specific tag."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        # Create a text tag
        tag_repo = TagRepository()
        text_tag = tag_repo.create_tag(name="Brand", value_type="text")
        
        # Create some text values for this tag
        value_repo = ValueRepository()
        value1 = value_repo.create_value(
            tag_id=text_tag.tag_id,
            value="Apple",
            value_type="text"
        )
        value2 = value_repo.create_value(
            tag_id=text_tag.tag_id,
            value="Samsung",
            value_type="text"
        )
        value3 = value_repo.create_value(
            tag_id=text_tag.tag_id,
            value="Google",
            value_type="text"
        )
        
        # Get values for this tag
        response = client.get(f'/api/v1/value/tag/{text_tag.tag_id}', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Check that all values have the correct structure
        name_vals = [v['name_val'] for v in data]
        assert 'Apple' in name_vals
        assert 'Samsung' in name_vals
        assert 'Google' in name_vals

    def test_get_text_values_by_tag_filters_non_text_tags(
        self, client, verified_user, app_context, db_session
    ):
        """Test that only text values are returned, not boolean/numeric."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        # Create tags of different types
        tag_repo = TagRepository()
        text_tag = tag_repo.create_tag(name="Color", value_type="text")
        bool_tag = tag_repo.create_tag(name="Available", value_type="boolean")
        
        # Create values
        value_repo = ValueRepository()
        text_val = value_repo.create_value(
            tag_id=text_tag.tag_id,
            value="Red",
            value_type="text"
        )
        bool_val = value_repo.create_value(
            tag_id=bool_tag.tag_id,
            value=True,
            value_type="boolean"
        )
        
        # Request values for the boolean tag should fail
        # (or return empty/404) since it's not a text tag
        response = client.get(
            f'/api/v1/value/tag/{bool_tag.tag_id}',
            headers=headers
        )
        
        assert response.status_code == 404

    def test_get_text_values_by_tag_not_found(
        self, client, verified_user, app_context, db_session
    ):
        """Test getting values for a non-existent tag."""
        tokens = TokenService.generate_tokens(verified_user)
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        
        response = client.get('/api/v1/value/tag/99999', headers=headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
