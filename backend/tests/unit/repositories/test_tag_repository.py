"""Unit tests for TagRepository."""
import pytest
from app.repositories.implementations.tag_repository import TagRepository
from app.models.tag import Tag


@pytest.mark.unit
@pytest.mark.repository
class TestTagRepository:
    """Test TagRepository methods."""

    def test_get_all_tags_empty(self, db_session):
        """Test getting all tags when database is empty."""
        repo = TagRepository()
        tags = repo.get_all_tags()
        assert tags == []

    def test_get_all_tags_returns_ordered_list(self, db_session):
        """Test that tags are returned ordered by name."""
        repo = TagRepository()
        
        # Create tags in random order
        tag1 = repo.create_tag(name="Zebra", value_type="text")
        tag2 = repo.create_tag(name="Apple", value_type="boolean")
        tag3 = repo.create_tag(name="Mango", value_type="numeric")
        
        tags = repo.get_all_tags()
        
        assert len(tags) == 3
        assert tags[0].name == "Apple"
        assert tags[1].name == "Mango"
        assert tags[2].name == "Zebra"

    def test_get_tag_by_id_success(self, db_session):
        """Test getting tag by valid ID."""
        repo = TagRepository()
        created_tag = repo.create_tag(name="Condition", value_type="text")
        
        retrieved_tag = repo.get_tag_by_id(created_tag.tag_id)
        
        assert retrieved_tag is not None
        assert retrieved_tag.tag_id == created_tag.tag_id
        assert retrieved_tag.name == "Condition"
        assert retrieved_tag.value_type == "text"

    def test_get_tag_by_id_not_found(self, db_session):
        """Test getting tag with non-existent ID."""
        repo = TagRepository()
        tag = repo.get_tag_by_id(99999)
        assert tag is None

    def test_get_tag_by_name_case_insensitive(self, db_session):
        """Test getting tag by name is case-insensitive."""
        repo = TagRepository()
        repo.create_tag(name="Available", value_type="boolean")
        
        # Test different cases
        tag1 = repo.get_tag_by_name("available")
        tag2 = repo.get_tag_by_name("AVAILABLE")
        tag3 = repo.get_tag_by_name("Available")
        
        assert tag1 is not None
        assert tag2 is not None
        assert tag3 is not None
        assert tag1.tag_id == tag2.tag_id == tag3.tag_id

    def test_get_tag_by_name_not_found(self, db_session):
        """Test getting tag with non-existent name."""
        repo = TagRepository()
        tag = repo.get_tag_by_name("NonExistent")
        assert tag is None

    def test_create_tag_text_type(self, db_session):
        """Test creating tag with text value type."""
        repo = TagRepository()
        tag = repo.create_tag(name="Material", value_type="text")
        
        assert tag.tag_id is not None
        assert tag.name == "Material"
        assert tag.value_type == "text"

    def test_create_tag_boolean_type(self, db_session):
        """Test creating tag with boolean value type."""
        repo = TagRepository()
        tag = repo.create_tag(name="Available", value_type="boolean")
        
        assert tag.tag_id is not None
        assert tag.name == "Available"
        assert tag.value_type == "boolean"

    def test_create_tag_numeric_type(self, db_session):
        """Test creating tag with numeric value type."""
        repo = TagRepository()
        tag = repo.create_tag(name="Price", value_type="numeric")
        
        assert tag.tag_id is not None
        assert tag.name == "Price"
        assert tag.value_type == "numeric"
