"""Unit tests for ItemService."""
import pytest
from app.services.item_service import ItemService
from app.repositories.implementations.item_repository import ItemRepository
from app.repositories.implementations.category_repository import CategoryRepository
from app.repositories.implementations.rotation_city_repository import RotationCityRepository
from app.repositories.implementations.user_repository import UserRepository
from app.models.category import Category
from app.models.rotation_city import RotationCity
from app.models.user import User


@pytest.mark.unit
@pytest.mark.service
class TestItemService:
    """Test ItemService methods."""

    def test_get_all_items_empty(self, db_session):
        """Test getting all items when none exist."""
        service = ItemService()
        items = service.get_all_items()
        assert items == []

    def test_get_all_items_returns_list(self, db_session):
        """Test getting all items returns proper list."""
        # Setup
        item_repo = ItemRepository()
        service = ItemService(item_repository=item_repo)
        
        # Create necessary dependencies
        from app.models.rotation_city import RotationCity
        city = RotationCity(name="Test City", time_zone="UTC")
        db_session.add(city)
        db_session.commit()
        db_session.refresh(city)
        
        user_repo = UserRepository()
        user = user_repo.create_user(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            rotation_city_id=city.city_id
        )
        
        # Create items
        item_repo.create_item(
            name="Item 1",
            location="Location 1",
            rotation_city_id=city.city_id,
            added_by_user_id=user.user_id
        )
        item_repo.create_item(
            name="Item 2",
            location="Location 2",
            rotation_city_id=city.city_id,
            added_by_user_id=user.user_id,
            walking_distance=100.0
        )
        
        items = service.get_all_items()
        
        assert len(items) == 2
        assert all(hasattr(item, 'item_id') for item in items)
        assert all(hasattr(item, 'name') for item in items)
        assert all(hasattr(item, 'location') for item in items)

    def test_get_item_by_id_success(self, db_session):
        """Test getting item by ID when it exists."""
        # Setup
        item_repo = ItemRepository()
        service = ItemService(item_repository=item_repo)
        
        # Create necessary dependencies
        from app.models.rotation_city import RotationCity
        city = RotationCity(name="Test City 2", time_zone="UTC")
        db_session.add(city)
        db_session.commit()
        db_session.refresh(city)
        
        user_repo = UserRepository()
        user = user_repo.create_user(
            email="test2@example.com",
            first_name="Test",
            last_name="User",
            rotation_city_id=city.city_id
        )
        
        # Create item
        item = item_repo.create_item(
            name="Test Item",
            location="Test Location",
            rotation_city_id=city.city_id,
            added_by_user_id=user.user_id,
            walking_distance=50.0
        )
        
        # Test
        retrieved_item = service.get_item_by_id(item.item_id)
        
        assert retrieved_item is not None
        assert retrieved_item.item_id == item.item_id
        assert retrieved_item.name == "Test Item"
        assert retrieved_item.location == "Test Location"
        assert retrieved_item.walking_distance == 50.0

    def test_get_item_by_id_not_found(self, db_session):
        """Test getting item by ID when it doesn't exist."""
        service = ItemService()
        
        with pytest.raises(ValueError) as exc_info:
            service.get_item_by_id(99999)
        
        assert "Item with ID 99999 not found" in str(exc_info.value)

    def test_get_item_by_id_validates_item_exists(self, db_session):
        """Test that get_item_by_id raises error for non-existent items."""
        item_repo = ItemRepository()
        service = ItemService(item_repository=item_repo)
        
        with pytest.raises(ValueError) as exc_info:
            service.get_item_by_id(12345)
        
        assert "not found" in str(exc_info.value).lower()
