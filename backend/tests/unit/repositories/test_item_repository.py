"""Unit tests for ItemRepository."""
import pytest
from app.repositories.implementations.item_repository import ItemRepository
from app.repositories.implementations.user_repository import UserRepository
from app.repositories.implementations.rotation_city_repository import RotationCityRepository


@pytest.mark.unit
@pytest.mark.repository
class TestItemRepository:
    """Test ItemRepository methods."""

    def test_create_item_with_required_fields(self, db_session, verified_user, rotation_city):
        """Test creating item with all required fields."""
        repo = ItemRepository()
        
        item = repo.create_item(
            name="Test Desk",
            location="Building A, Room 101",
            rotation_city_id=rotation_city.city_id,
            added_by_user_id=verified_user.user_id
        )
        
        assert item.item_id is not None
        assert item.name == "Test Desk"
        assert item.location == "Building A, Room 101"
        assert item.rotation_city_id == rotation_city.city_id
        assert item.added_by_user_id == verified_user.user_id
        assert item.walking_distance is None
        assert item.number_of_verifications == 0

    def test_create_item_with_walking_distance(self, db_session, verified_user, rotation_city):
        """Test creating item with walking distance."""
        repo = ItemRepository()
        
        item = repo.create_item(
            name="Library Desk",
            location="Library 3rd Floor",
            rotation_city_id=rotation_city.city_id,
            added_by_user_id=verified_user.user_id,
            walking_distance=150.5
        )
        
        assert item.item_id is not None
        assert item.walking_distance == 150.5

    def test_get_item_by_id_success(self, db_session, verified_user, rotation_city):
        """Test getting item by valid ID."""
        repo = ItemRepository()
        
        created_item = repo.create_item(
            name="Test Item",
            location="Test Location",
            rotation_city_id=rotation_city.city_id,
            added_by_user_id=verified_user.user_id
        )
        
        retrieved_item = repo.get_item_by_id(created_item.item_id)
        
        assert retrieved_item is not None
        assert retrieved_item.item_id == created_item.item_id
        assert retrieved_item.name == "Test Item"

    def test_get_item_by_id_not_found(self, db_session):
        """Test getting item with non-existent ID."""
        repo = ItemRepository()
        item = repo.get_item_by_id(99999)
        assert item is None

    def test_create_multiple_items(self, db_session, verified_user, rotation_city):
        """Test creating multiple items."""
        repo = ItemRepository()
        
        item1 = repo.create_item(
            name="Item 1",
            location="Location 1",
            rotation_city_id=rotation_city.city_id,
            added_by_user_id=verified_user.user_id
        )
        
        item2 = repo.create_item(
            name="Item 2",
            location="Location 2",
            rotation_city_id=rotation_city.city_id,
            added_by_user_id=verified_user.user_id
        )
        
        assert item1.item_id != item2.item_id
        assert item1.name == "Item 1"
        assert item2.name == "Item 2"
