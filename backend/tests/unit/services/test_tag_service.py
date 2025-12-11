"""Unit tests for TagService."""
import pytest
from app.services.tag_service import TagService
from app.repositories.implementations.tag_repository import TagRepository
from app.models.tag import TagValueType


@pytest.mark.unit
@pytest.mark.service
class TestTagService:
    """Test TagService methods."""

    def test_get_all_tags_empty(self, db_session):
        """Test getting all tags when none exist."""
        service = TagService()
        tags = service.get_all_tags()
        assert tags == []

    def test_get_all_tags_returns_list(self, db_session):
        """Test getting all tags returns proper list."""
        tag_repo = TagRepository()
        service = TagService(tag_repo)
        
        # Create some tags
        tag_repo.create_tag(name="Condition", value_type=TagValueType.TEXT.code)
        tag_repo.create_tag(name="Available", value_type=TagValueType.BOOLEAN.code)
        tag_repo.create_tag(name="Price", value_type=TagValueType.NUMERIC.code)
        
        tags = service.get_all_tags()
        
        assert len(tags) == 3
        assert all(hasattr(tag, 'tag_id') for tag in tags)
        assert all(hasattr(tag, 'name') for tag in tags)
        assert all(hasattr(tag, 'value_type') for tag in tags)

    def test_get_all_tags_ordered_by_name(self, db_session):
        """Test that tags are returned in alphabetical order."""
        tag_repo = TagRepository()
        service = TagService(tag_repo)
        
        # Create tags in non-alphabetical order
        tag_repo.create_tag(name="Zebra", value_type=TagValueType.TEXT.code)
        tag_repo.create_tag(name="Apple", value_type=TagValueType.TEXT.code)
        tag_repo.create_tag(name="Banana", value_type=TagValueType.TEXT.code)
        
        tags = service.get_all_tags()
        
        assert tags[0].name == "Apple"
        assert tags[1].name == "Banana"
        assert tags[2].name == "Zebra"
