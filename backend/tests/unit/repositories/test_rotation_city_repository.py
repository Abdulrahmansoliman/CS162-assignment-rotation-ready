"""
Unit tests for RotationCityRepository.
"""
import pytest
from app.repositories.implementations.rotation_city_repository import (
    RotationCityRepository
)
from app.models.rotation_city import RotationCity


@pytest.mark.unit
@pytest.mark.repository
class TestRotationCityRepository:
    """Test cases for RotationCityRepository."""

    @pytest.fixture
    def repository(self):
        """Provide a repository instance for each test."""
        return RotationCityRepository()

    def test_get_rotation_city_by_id_when_exists(
        self,
        db_session,
        repository,
        rotation_city
    ):
        """Test retrieving rotation city by ID when it exists."""
        result = repository.get_rotation_city_by_id(rotation_city.city_id)

        assert result is not None
        assert result.city_id == rotation_city.city_id
        assert result.name == rotation_city.name

    def test_get_rotation_city_by_id_when_not_exists(
        self,
        db_session,
        repository
    ):
        """Test retrieving rotation city by ID when it doesn't exist."""
        result = repository.get_rotation_city_by_id(99999)

        assert result is None

    def test_get_all_rotation_cities_returns_empty_when_none(
        self,
        db_session,
        repository
    ):
        """Test getting all rotation cities when database is empty."""
        result = repository.get_all_rotation_cities()

        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_all_rotation_cities_returns_all(
        self,
        db_session,
        repository
    ):
        """Test getting all rotation cities returns all created cities."""
        # Create test cities
        city1 = RotationCity(
            name="San Francisco",
            time_zone="America/Los_Angeles",
            res_hall_location="123 Market St"
        )
        city2 = RotationCity(
            name="Berlin",
            time_zone="Europe/Berlin",
            res_hall_location="456 Brandenburg St"
        )
        db_session.add(city1)
        db_session.add(city2)
        db_session.commit()

        result = repository.get_all_rotation_cities()

        assert len(result) == 2
        assert all(isinstance(c, RotationCity) for c in result)

    def test_get_rotation_city_by_name_when_exists(
        self,
        db_session,
        repository,
        rotation_city
    ):
        """Test retrieving rotation city by name when it exists."""
        result = repository.get_rotation_city_by_name(rotation_city.name)

        assert result is not None
        assert result.city_id == rotation_city.city_id
        assert result.name == rotation_city.name

    def test_get_rotation_city_by_name_when_not_exists(
        self,
        db_session,
        repository
    ):
        """Test retrieving rotation city by name when it doesn't exist."""
        result = repository.get_rotation_city_by_name("Nonexistent City")

        assert result is None

    def test_get_rotation_city_by_name_case_sensitive(
        self,
        db_session,
        repository,
        rotation_city
    ):
        """Test that name search is case-sensitive."""
        result = repository.get_rotation_city_by_name(
            rotation_city.name.upper()
        )

        # Should not find if case doesn't match
        if rotation_city.name != rotation_city.name.upper():
            assert result is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
