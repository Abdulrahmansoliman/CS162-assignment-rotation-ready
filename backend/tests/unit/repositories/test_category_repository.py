"""
Unit tests for CategoryRepository with mocked database
"""
import pytest
from unittest.mock import Mock, MagicMock
from app.repositories.implementations.category_repository import CategoryRepository
from app.models.category import Category


@pytest.mark.unit
@pytest.mark.repository
class TestCategoryRepository:
    """Test cases for CategoryRepository with mocked database"""

    @pytest.fixture
    def mock_db_session(self, mocker):
        """Mock database session"""
        return mocker.patch('app.repositories.implementations.category_repository.db.session')

    @pytest.fixture
    def repository(self):
        """Create repository instance"""
        return CategoryRepository()

    def test_get_all_categories_success(self, repository, mock_db_session):
        """Test get_all_categories returns list of categories"""
        # Arrange
        mock_categories = [
            Category(category_id=1, category_name="Electronics", category_pic="pic1.jpg"),
            Category(category_id=2, category_name="Books", category_pic="pic2.jpg")
        ]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_categories
        mock_db_session.execute.return_value = mock_result

        # Act
        result = repository.get_all_categories()

        # Assert
        assert len(result) == 2
        assert result[0].category_name == "Electronics"
        assert result[1].category_name == "Books"
        mock_db_session.execute.assert_called_once()

    def test_get_all_categories_empty(self, repository, mock_db_session):
        """Test get_all_categories returns empty list when no categories"""
        # Arrange
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute.return_value = mock_result

        # Act
        result = repository.get_all_categories()

        # Assert
        assert result == []
        mock_db_session.execute.assert_called_once()

    def test_get_category_by_id_success(self, repository, mock_db_session):
        """Test get_category_by_id returns category when found"""
        # Arrange
        mock_category = Category(category_id=1, category_name="Electronics", category_pic="pic.jpg")
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_category
        mock_db_session.execute.return_value = mock_result

        # Act
        result = repository.get_category_by_id(1)

        # Assert
        assert result.category_id == 1
        assert result.category_name == "Electronics"
        mock_db_session.execute.assert_called_once()

    def test_get_category_by_id_not_found(self, repository, mock_db_session):
        """Test get_category_by_id returns None when not found"""
        # Arrange
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        # Act
        result = repository.get_category_by_id(999)

        # Assert
        assert result is None
        mock_db_session.execute.assert_called_once()

    def test_add_category_success(self, repository, mock_db_session):
        """Test add_category creates new category"""
        # Arrange
        mock_db_session.commit.return_value = None

        # Act
        result = repository.add_category(name="Electronics", pic="pic.jpg")

        # Assert
        assert result is not None
        assert result.category_name == "Electronics"
        assert result.category_pic == "pic.jpg"
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    def test_add_category_no_pic(self, repository, mock_db_session):
        """Test add_category works without picture"""
        # Arrange
        mock_db_session.commit.return_value = None

        # Act
        result = repository.add_category(name="Books", pic=None)

        # Assert
        assert result is not None
        assert result.category_name == "Books"
        assert result.category_pic is None
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    def test_add_category_failure(self, repository, mock_db_session):
        """Test add_category handles database errors"""
        # Arrange
        mock_db_session.commit.side_effect = Exception("Database error")

        # Act
        result = repository.add_category(name="Electronics", pic="pic.jpg")

        # Assert
        assert result is None
        mock_db_session.rollback.assert_called_once()

    def test_update_category_success(self, repository, mock_db_session):
        """Test update_category updates existing category"""
        # Arrange
        mock_category = Category(category_id=1, category_name="Old Name", category_pic="old.jpg")
        mock_db_session.get.return_value = mock_category

        # Act
        result = repository.update_category(category_id=1, name="New Name", pic="new.jpg")

        # Assert
        assert result.category_name == "New Name"
        assert result.category_pic == "new.jpg"
        mock_db_session.commit.assert_called_once()

    def test_update_category_partial(self, repository, mock_db_session):
        """Test update_category allows partial updates"""
        # Arrange
        mock_category = Category(category_id=1, category_name="Old Name", category_pic="old.jpg")
        mock_db_session.get.return_value = mock_category

        # Act - only update name
        result = repository.update_category(category_id=1, name="New Name", pic=None)

        # Assert
        assert result.category_name == "New Name"
        assert result.category_pic == "old.jpg"  # Unchanged
        mock_db_session.commit.assert_called_once()

    def test_update_category_not_found(self, repository, mock_db_session):
        """Test update_category returns None when category not found"""
        # Arrange
        mock_db_session.get.return_value = None

        # Act
        result = repository.update_category(category_id=999, name="New Name")

        # Assert
        assert result is None
        mock_db_session.commit.assert_not_called()

    def test_update_category_failure(self, repository, mock_db_session):
        """Test update_category handles database errors"""
        # Arrange
        mock_category = Category(category_id=1, category_name="Old Name")
        mock_db_session.get.return_value = mock_category
        mock_db_session.commit.side_effect = Exception("Database error")

        # Act
        result = repository.update_category(category_id=1, name="New Name")

        # Assert
        assert result is None
        mock_db_session.rollback.assert_called_once()

    def test_delete_category_success(self, repository, mock_db_session):
        """Test delete_category removes category"""
        # Arrange
        mock_category = Category(category_id=1, category_name="Electronics")
        mock_db_session.get.return_value = mock_category

        # Act
        result = repository.delete_category(category_id=1)

        # Assert
        assert result is True
        mock_db_session.delete.assert_called_once_with(mock_category)
        mock_db_session.commit.assert_called_once()

    def test_delete_category_not_found(self, repository, mock_db_session):
        """Test delete_category returns False when category not found"""
        # Arrange
        mock_db_session.get.return_value = None

        # Act
        result = repository.delete_category(category_id=999)

        # Assert
        assert result is False
        mock_db_session.delete.assert_not_called()
        mock_db_session.commit.assert_not_called()

    def test_delete_category_failure(self, repository, mock_db_session):
        """Test delete_category handles database errors"""
        # Arrange
        mock_category = Category(category_id=1, category_name="Electronics")
        mock_db_session.get.return_value = mock_category
        mock_db_session.commit.side_effect = Exception("Database error")

        # Act
        result = repository.delete_category(category_id=1)

        # Assert
        assert result is False
        mock_db_session.rollback.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])