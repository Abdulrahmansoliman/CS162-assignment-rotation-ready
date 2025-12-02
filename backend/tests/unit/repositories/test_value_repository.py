"""
Unit tests for ValueRepository.
"""
import pytest
from app.repositories.implementations.value_repository import (
    ValueRepository
)
from app.models.value import Value


@pytest.mark.unit
@pytest.mark.repository
class TestValueRepository:

    @pytest.fixture
    def repository(self):
        """Provide a repository instance for each test"""
        return ValueRepository()