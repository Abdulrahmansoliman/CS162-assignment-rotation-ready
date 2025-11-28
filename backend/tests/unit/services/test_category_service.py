"""
Unit tests for CategoryService with mocked dependencies
"""
import pytest
from unittest.mock import Mock
from app.services.category_service import CategoryService
from app.models.category import Category


@pytest.mark.unit
@pytest.mark.service
class TestCategoryService:
    """Test cases for CategoryService with dependency injection"""

    @pytest.fixture
    def mock_repository(self):
        """Create mock repository"""
        return Mock()

    @pytest.fixture
    def service(self, mock_repository):
        """Create service with mocked repository"""
        return CategoryService(category_repository=mock_repository)

    def test_get_all_categories_success(self, service, mock_repository):
        """Test get_all_categories returns list of categories"""
        # Arrange
        mock_categories = [
            Category(category_id=1, category_name="Electronics"),
            Category(category_id=2, category_name="Books")
        ]
        mock_repository.get_all_categories.return_value = mock_categories

        # Act
        result = service.get_all_categories()

        # Assert
        assert len(result) == 2
        assert result[0].category_name == "Electronics"
        mock_repository.get_all_categories.assert_called_once()

    def test_get_all_categories_empty(self, service, mock_repository):
        """Test get_all_categories returns empty list"""
        # Arrange
        mock_repository.get_all_categories.return_value = []

        # Act
        result = service.get_all_categories()

        # Assert
        assert result == []
        mock_repository.get_all_categories.assert_called_once()

    def test_get_category_by_id_success(self, service, mock_repository):
        """Test get_category_by_id returns category"""
        # Arrange
        mock_category = Category(category_id=1, category_name="Electronics")
        mock_repository.get_category_by_id.return_value = mock_category

        # Act
        result = service.get_category_by_id(1)

        # Assert
        assert result.category_id == 1
        assert result.category_name == "Electronics"
        mock_repository.get_category_by_id.assert_called_once_with(1)

    def test_get_category_by_id_not_found(self, service, mock_repository):
        """Test get_category_by_id returns None when not found"""
        # Arrange
        mock_repository.get_category_by_id.return_value = None

        # Act
        result = service.get_category_by_id(999)

        # Assert
        assert result is None
        mock_repository.get_category_by_id.assert_called_once_with(999)

    def test_add_category_success(self, service, mock_repository):
        """Test add_category creates new category"""
        # Arrange
        mock_category = Category(category_id=1, category_name="Electronics", category_pic="pic.jpg")
        mock_repository.add_category.return_value = mock_category

        # Act
        result = service.add_category(category_name="Electronics", category_pic="pic.jpg")

        # Assert
        assert result.category_name == "Electronics"
        assert result.category_pic == "pic.jpg"
        mock_repository.add_category.assert_called_once_with("Electronics", "pic.jpg")

    def test_add_category_no_pic(self, service, mock_repository):
        """Test add_category works without picture"""
        # Arrange
        mock_category = Category(category_id=1, category_name="Books", category_pic=None)
        mock_repository.add_category.return_value = mock_category

        # Act
        result = service.add_category(category_name="Books", category_pic=None)

        # Assert
        assert result.category_name == "Books"
        assert result.category_pic is None
        mock_repository.add_category.assert_called_once_with("Books", None)

    def test_update_category_success(self, service, mock_repository):
        """Test update_category updates category"""
        # Arrange
        mock_category = Category(category_id=1, category_name="New Name", category_pic="new.jpg")
        mock_repository.update_category.return_value = mock_category

        # Act
        result = service.update_category(category_id=1, category_name="New Name", category_pic="new.jpg")

        # Assert
        assert result.category_name == "New Name"
        assert result.category_pic == "new.jpg"
        mock_repository.update_category.assert_called_once_with(1, "New Name", "new.jpg")

    def test_update_category_partial(self, service, mock_repository):
        """Test update_category allows partial updates"""
        # Arrange
        mock_category = Category(category_id=1, category_name="New Name", category_pic="old.jpg")
        mock_repository.update_category.return_value = mock_category

        # Act
        result = service.update_category(category_id=1, category_name="New Name", category_pic=None)

        # Assert
        assert result.category_name == "New Name"
        mock_repository.update_category.assert_called_once_with(1, "New Name", None)

    def test_update_category_not_found(self, service, mock_repository):
        """Test update_category returns None when not found"""
        # Arrange
        mock_repository.update_category.return_value = None

        # Act
        result = service.update_category(category_id=999, category_name="New Name")

        # Assert
        assert result is None
        mock_repository.update_category.assert_called_once_with(999, "New Name", None)

    def test_delete_category_success(self, service, mock_repository):
        """Test delete_category removes category"""
        # Arrange
        mock_repository.delete_category.return_value = True

        # Act
        result = service.delete_category(category_id=1)

        # Assert
        assert result is True
        mock_repository.delete_category.assert_called_once_with(1)

    def test_delete_category_not_found(self, service, mock_repository):
        """Test delete_category returns False when not found"""
        # Arrange
        mock_repository.delete_category.return_value = False

        # Act
        result = service.delete_category(category_id=999)

        # Assert
        assert result is False
        mock_repository.delete_category.assert_called_once_with(999)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])