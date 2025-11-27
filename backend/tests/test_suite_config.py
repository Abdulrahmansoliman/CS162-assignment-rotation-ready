"""
Test Suite Configuration

Defines test categories, markers, and execution configurations for the test suite.
This module provides centralized configuration for all test execution strategies.
"""
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class TestCategory(Enum):
    """Enumeration of available test categories."""
    UNIT = "unit"
    INTEGRATION = "integration"
    API = "api"
    MODEL = "model"
    REPOSITORY = "repository"
    SERVICE = "service"
    ALL = "all"


class TestLevel(Enum):
    """Test execution levels for different scopes."""
    FAST = "fast"           # Unit tests only
    MEDIUM = "medium"       # Unit + Integration
    FULL = "full"          # All tests including slow ones
    SMOKE = "smoke"        # Critical path tests only


@dataclass
class TestSuiteConfig:
    """Configuration for test suite execution."""
    
    # Test discovery paths
    UNIT_TEST_PATH: str = "tests/unit"
    INTEGRATION_TEST_PATH: str = "tests/integration"
    
    # Pytest markers
    UNIT_MARKER: str = "unit"
    INTEGRATION_MARKER: str = "integration"
    API_MARKER: str = "api"
    MODEL_MARKER: str = "model"
    REPOSITORY_MARKER: str = "repository"
    SERVICE_MARKER: str = "service"
    SMOKE_MARKER: str = "smoke"
    SLOW_MARKER: str = "slow"
    
    # Default pytest arguments
    DEFAULT_ARGS: List[str] = None
    
    # Output settings
    VERBOSE: bool = True
    SHOW_LOCALS: bool = False
    TRACEBACK_STYLE: str = "short"  # short, long, line, native, no
    
    # Coverage settings
    ENABLE_COVERAGE: bool = False
    COVERAGE_MIN_PERCENTAGE: float = 80.0
    
    # Performance settings
    MAX_WORKERS: int = 4  # For parallel execution
    
    def __post_init__(self):
        """Initialize default arguments if not provided."""
        if self.DEFAULT_ARGS is None:
            self.DEFAULT_ARGS = [
                "-v",                    # Verbose
                "--tb=short",            # Short traceback
                "--strict-markers",      # Strict marker checking
                "--disable-warnings",    # Disable warnings in output
            ]
    
    def get_marker_expression(self, categories: List[TestCategory]) -> Optional[str]:
        """
        Build pytest marker expression from test categories.
        
        Args:
            categories: List of test categories to include
            
        Returns:
            Marker expression string or None for all tests
        """
        if not categories or TestCategory.ALL in categories:
            return None
        
        markers = []
        for category in categories:
            if category == TestCategory.UNIT:
                markers.append(self.UNIT_MARKER)
            elif category == TestCategory.INTEGRATION:
                markers.append(self.INTEGRATION_MARKER)
            elif category == TestCategory.API:
                markers.append(self.API_MARKER)
            elif category == TestCategory.MODEL:
                markers.append(self.MODEL_MARKER)
            elif category == TestCategory.REPOSITORY:
                markers.append(self.REPOSITORY_MARKER)
            elif category == TestCategory.SERVICE:
                markers.append(self.SERVICE_MARKER)
        
        return " or ".join(markers) if markers else None
    
    def get_test_paths(self, categories: List[TestCategory]) -> List[str]:
        """
        Get test paths based on categories.
        
        Args:
            categories: List of test categories
            
        Returns:
            List of paths to search for tests
        """
        if not categories or TestCategory.ALL in categories:
            return ["tests/"]
        
        paths = []
        if TestCategory.UNIT in categories:
            paths.append(self.UNIT_TEST_PATH)
        if TestCategory.INTEGRATION in categories or TestCategory.API in categories:
            paths.append(self.INTEGRATION_TEST_PATH)
        
        return paths if paths else ["tests/"]


config = TestSuiteConfig()
