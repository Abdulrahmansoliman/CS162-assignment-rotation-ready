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

    def test_find_similar_text_values_exact_match(self, db_session):
        """Test finding similar text values with exact match."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Brand", value_type="text")
        value1 = value_repo.create_value(tag.tag_id, "Samsung", "text")
        value2 = value_repo.create_value(tag.tag_id, "Apple", "text")
        value3 = value_repo.create_value(tag.tag_id, "Sony", "text")
        
        results = value_repo.find_similar_text_values(tag.tag_id, "Samsung")
        
        assert len(results) == 1
        assert results[0].name_val == "Samsung"
        assert results[0].value_id == value1.value_id

    def test_find_similar_text_values_partial_match(self, db_session):
        """Test finding similar text values with partial match."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Brand", value_type="text")
        value1 = value_repo.create_value(tag.tag_id, "Samsung Galaxy", "text")
        value2 = value_repo.create_value(tag.tag_id, "Samsung Note", "text")
        value3 = value_repo.create_value(tag.tag_id, "Apple iPhone", "text")
        
        results = value_repo.find_similar_text_values(tag.tag_id, "Samsung")
        
        assert len(results) == 2
        names = [v.name_val for v in results]
        assert "Samsung Galaxy" in names
        assert "Samsung Note" in names

    def test_find_similar_text_values_case_insensitive(self, db_session):
        """Test that similar value search is case-insensitive."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Color", value_type="text")
        value1 = value_repo.create_value(tag.tag_id, "Red", "text")
        value2 = value_repo.create_value(tag.tag_id, "Blue", "text")
        
        # Search with lowercase
        results = value_repo.find_similar_text_values(tag.tag_id, "red")
        
        assert len(results) == 1
        assert results[0].name_val == "Red"

    def test_find_similar_text_values_empty_result(self, db_session):
        """Test finding similar values with no matches."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag = tag_repo.create_tag(name="Material", value_type="text")
        value1 = value_repo.create_value(tag.tag_id, "Wood", "text")
        value2 = value_repo.create_value(tag.tag_id, "Metal", "text")
        
        results = value_repo.find_similar_text_values(tag.tag_id, "Plastic")
        
        assert len(results) == 0

    def test_find_similar_text_values_filters_by_tag(self, db_session):
        """Test that similar value search filters by tag."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        tag1 = tag_repo.create_tag(name="Material", value_type="text")
        tag2 = tag_repo.create_tag(name="Color", value_type="text")
        
        value1 = value_repo.create_value(tag1.tag_id, "Leather", "text")
        value2 = value_repo.create_value(tag2.tag_id, "Leather Jacket", "text")
        
        results = value_repo.find_similar_text_values(tag1.tag_id, "Leather")
        
        assert len(results) == 1
        assert results[0].value_id == value1.value_id
        assert results[0].tag_id == tag1.tag_id

    def test_find_similar_text_values_ignores_non_text_tags(self, db_session):
        """Test that similar value search only returns text tags."""
        tag_repo = TagRepository()
        value_repo = ValueRepository()
        
        text_tag = tag_repo.create_tag(name="Brand", value_type="text")
        bool_tag = tag_repo.create_tag(name="Available", value_type="boolean")
        
        text_value = value_repo.create_value(text_tag.tag_id, "Samsung", "text")
        bool_value = value_repo.create_value(bool_tag.tag_id, True, "boolean")
        
        # Try to search from boolean tag - should return empty
        results = value_repo.find_similar_text_values(bool_tag.tag_id, "Sam")
        
        assert len(results) == 0
