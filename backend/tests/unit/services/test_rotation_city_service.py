"""
Unit tests for RotationCityService with mocked dependencies.
"""
import pytest
from unittest.mock import Mock
from app.services.rotation_city_service import RotationCityService
from app.models.rotation_city import RotationCity


@pytest.mark.unit
@pytest.mark.service
class TestRotationCityService:
    """Test cases for RotationCityService with dependency injection."""

    @pytest.fixture
    def mock_repo(self):
        """Provide a mocked RotationCityRepository."""
        return Mock()

    @pytest.fixture
    def service(self, mock_repo):
        """Provide RotationCityService with mocked repository."""
        return RotationCityService(rotation_city_repository=mock_repo)

    def test_get_rotation_city_success(self, service, mock_repo):
        """Test successful retrieval of rotation city by ID."""
        # Arrange
        mock_city = RotationCity(
            city_id=1,
            name="San Francisco",
            time_zone="America/Los_Angeles",
            res_hall_location="123 Market St"
        )
        mock_repo.get_rotation_city_by_id.return_value = mock_city

        # Act
        result = service.get_rotation_city(city_id=1)

        # Assert
        assert result is not None
        assert result.name == "San Francisco"
        mock_repo.get_rotation_city_by_id.assert_called_once_with(1)

    def test_get_rotation_city_not_found(self, service, mock_repo):
        """Test retrieval of non-existent rotation city."""
        # Arrange
        mock_repo.get_rotation_city_by_id.return_value = None

        # Act
        result = service.get_rotation_city(city_id=99999)

        # Assert
        assert result is None
        mock_repo.get_rotation_city_by_id.assert_called_once_with(99999)

    def test_get_all_rotation_cities_success(self, service, mock_repo):
        """Test successful retrieval of all rotation cities."""
        # Arrange
        mock_cities = [
            RotationCity(
                city_id=1,
                name="San Francisco",
                time_zone="America/Los_Angeles"
            ),
            RotationCity(
                city_id=2,
                name="Berlin",
                time_zone="Europe/Berlin"
            )
        ]
        mock_repo.get_all_rotation_cities.return_value = mock_cities

        # Act
        result = service.get_all_rotation_cities()

        # Assert
        assert len(result) == 2
        assert result[0].name == "San Francisco"
        assert result[1].name == "Berlin"
        mock_repo.get_all_rotation_cities.assert_called_once()

    def test_get_all_rotation_cities_empty(self, service, mock_repo):
        """Test retrieval of rotation cities when none exist."""
        # Arrange
        mock_repo.get_all_rotation_cities.return_value = []

        # Act
        result = service.get_all_rotation_cities()

        # Assert
        assert len(result) == 0
        mock_repo.get_all_rotation_cities.assert_called_once()

    def test_get_rotation_city_by_name_success(self, service, mock_repo):
        """Test successful retrieval of rotation city by name."""
        # Arrange
        mock_city = RotationCity(
            city_id=1,
            name="Berlin",
            time_zone="Europe/Berlin"
        )
        mock_repo.get_rotation_city_by_name.return_value = mock_city

        # Act
        result = service.get_rotation_city_by_name(name="Berlin")

        # Assert
        assert result is not None
        assert result.name == "Berlin"
        mock_repo.get_rotation_city_by_name.assert_called_once_with("Berlin")

    def test_get_rotation_city_by_name_not_found(
        self,
        service,
        mock_repo
    ):
        """Test retrieval of rotation city by non-existent name."""
        # Arrange
        mock_repo.get_rotation_city_by_name.return_value = None

        # Act
        result = service.get_rotation_city_by_name(name="Nonexistent")

        # Assert
        assert result is None
        mock_repo.get_rotation_city_by_name.assert_called_once_with(
            "Nonexistent"
        )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
