"""Unit tests for ValueRepository."""
import pytest
from app.repositories.implementations.value_repository import ValueRepository
from app.repositories.implementations.tag_repository import TagRepository


@pytest.mark.unit
@pytest.mark.repository
class TestValueRepository:
    """Test ValueRepository methods."""

    def test_create_value_boolean(self, db_session):
        """Test creating boolean value."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Available", value_type="boolean")
        value = value_repo.create_value(tag.tag_id, True, "boolean")
        
        assert value.value_id is not None
        assert value.tag_id == tag.tag_id
        assert value.boolean_val is True
        assert value.name_val is None
        assert value.numerical_value is None

    def test_create_value_text(self, db_session):
        """Test creating text value."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Condition", value_type="text")
        value = value_repo.create_value(tag.tag_id, "Excellent", "text")
        
        assert value.value_id is not None
        assert value.tag_id == tag.tag_id
        assert value.boolean_val is None
        assert value.name_val == "Excellent"
        assert value.numerical_value is None

    def test_create_value_numeric(self, db_session):
        """Test creating numeric value."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Price", value_type="numeric")
        value = value_repo.create_value(tag.tag_id, 99.99, "numeric")
        
        assert value.value_id is not None
        assert value.tag_id == tag.tag_id
        assert value.boolean_val is None
        assert value.name_val is None
        assert value.numerical_value == 99.99

    def test_get_value_by_id_success(self, db_session):
        """Test getting value by valid ID."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Test", value_type="text")
        created_value = value_repo.create_value(tag.tag_id, "TestValue", "text")
        
        retrieved_value = value_repo.get_value_by_id(created_value.value_id)
        
        assert retrieved_value is not None
        assert retrieved_value.value_id == created_value.value_id
        assert retrieved_value.name_val == "TestValue"

    def test_get_value_by_id_not_found(self, db_session):
        """Test getting value with non-existent ID."""
        value_repo = ValueRepository()
        value = value_repo.get_value_by_id(99999)
        assert value is None

    def test_find_existing_value_boolean(self, db_session):
        """Test finding existing boolean value."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Available", value_type="boolean")
        created_value = value_repo.create_value(tag.tag_id, True, "boolean")
        
        found_value = value_repo.find_existing_value(tag.tag_id, True, "boolean")
        
        assert found_value is not None
        assert found_value.value_id == created_value.value_id

    def test_find_existing_value_text(self, db_session):
        """Test finding existing text value."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Material", value_type="text")
        created_value = value_repo.create_value(tag.tag_id, "Wood", "text")
        
        found_value = value_repo.find_existing_value(tag.tag_id, "Wood", "text")
        
        assert found_value is not None
        assert found_value.value_id == created_value.value_id

    def test_find_existing_value_numeric(self, db_session):
        """Test finding existing numeric value."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Height", value_type="numeric")
        created_value = value_repo.create_value(tag.tag_id, 75.5, "numeric")
        
        found_value = value_repo.find_existing_value(tag.tag_id, 75.5, "numeric")
        
        assert found_value is not None
        assert found_value.value_id == created_value.value_id

    def test_find_existing_value_not_found(self, db_session):
        """Test finding non-existent value."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Test", value_type="text")
        
        found_value = value_repo.find_existing_value(tag.tag_id, "NonExistent", "text")
        
        assert found_value is None

    def test_create_multiple_values_for_same_tag(self, db_session):
        """Test creating multiple different values for same tag."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Condition", value_type="text")
        value1 = value_repo.create_value(tag.tag_id, "Excellent", "text")
        value2 = value_repo.create_value(tag.tag_id, "Good", "text")
        value3 = value_repo.create_value(tag.tag_id, "Fair", "text")
        
        assert value1.value_id != value2.value_id != value3.value_id
        assert value1.tag_id == value2.tag_id == value3.tag_id == tag.tag_id
