"""
Test Execution Strategies

Implements the Strategy Pattern for different test execution approaches.
Each strategy defines how tests should be discovered, filtered, and executed.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
import subprocess
import sys
from pathlib import Path

from tests.test_suite_config import TestCategory, TestLevel, config


class TestExecutionStrategy(ABC):
    """Abstract base class for test execution strategies."""
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the execution strategy.
        
        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.config = config
    
    @abstractmethod
    def build_pytest_args(self) -> List[str]:
        """
        Build pytest command-line arguments.
        
        Returns:
            List of pytest arguments
        """
        pass
    
    def execute(self) -> int:
        """
        Execute tests using this strategy.
        
        Returns:
            Exit code from pytest (0 for success, non-zero for failure)
        """
        args = self.build_pytest_args()
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"Executing: pytest {' '.join(args)}")
            print(f"{'='*70}\n")
        
        # Run pytest programmatically
        import pytest
        return pytest.main(args)


class AllTestsStrategy(TestExecutionStrategy):
    """Strategy to execute all tests in the suite."""
    
    def build_pytest_args(self) -> List[str]:
        """Build arguments to run all tests."""
        args = self.config.DEFAULT_ARGS.copy()
        args.append("tests/")
        return args


class UnitTestsStrategy(TestExecutionStrategy):
    """Strategy to execute only unit tests."""
    
    def build_pytest_args(self) -> List[str]:
        """Build arguments to run unit tests only."""
        args = self.config.DEFAULT_ARGS.copy()
        args.extend([
            "-m", self.config.UNIT_MARKER,
            self.config.UNIT_TEST_PATH
        ])
        return args


class IntegrationTestsStrategy(TestExecutionStrategy):
    """Strategy to execute only integration tests."""
    
    def build_pytest_args(self) -> List[str]:
        """Build arguments to run integration tests only."""
        args = self.config.DEFAULT_ARGS.copy()
        args.extend([
            "-m", self.config.INTEGRATION_MARKER,
            self.config.INTEGRATION_TEST_PATH
        ])
        return args


class CategoryBasedStrategy(TestExecutionStrategy):
    """Strategy to execute tests based on specific categories."""
    
    def __init__(self, categories: List[TestCategory], verbose: bool = True):
        """
        Initialize category-based strategy.
        
        Args:
            categories: List of test categories to execute
            verbose: Enable verbose output
        """
        super().__init__(verbose)
        self.categories = categories
    
    def build_pytest_args(self) -> List[str]:
        """Build arguments based on specified categories."""
        args = self.config.DEFAULT_ARGS.copy()
        
        # Get marker expression
        marker_expr = self.config.get_marker_expression(self.categories)
        if marker_expr:
            args.extend(["-m", marker_expr])
        
        # Get test paths
        paths = self.config.get_test_paths(self.categories)
        args.extend(paths)
        
        return args


class LevelBasedStrategy(TestExecutionStrategy):
    """Strategy to execute tests based on test level (fast, medium, full)."""
    
    def __init__(self, level: TestLevel, verbose: bool = True):
        """
        Initialize level-based strategy.
        
        Args:
            level: Test execution level
            verbose: Enable verbose output
        """
        super().__init__(verbose)
        self.level = level
    
    def build_pytest_args(self) -> List[str]:
        """Build arguments based on execution level."""
        args = self.config.DEFAULT_ARGS.copy()
        
        if self.level == TestLevel.FAST:
            # Only unit tests
            args.extend(["-m", self.config.UNIT_MARKER])
            args.append(self.config.UNIT_TEST_PATH)
        
        elif self.level == TestLevel.MEDIUM:
            # Unit and integration, exclude slow tests
            args.extend(["-m", f"not {self.config.SLOW_MARKER}"])
            args.append("tests/")
        
        elif self.level == TestLevel.FULL:
            # All tests including slow ones
            args.append("tests/")
        
        elif self.level == TestLevel.SMOKE:
            # Only smoke tests
            args.extend(["-m", self.config.SMOKE_MARKER])
            args.append("tests/")
        
        return args


class ParallelExecutionStrategy(TestExecutionStrategy):
    """Strategy to execute tests in parallel using pytest-xdist."""
    
    def __init__(self, num_workers: Optional[int] = None, verbose: bool = True):
        """
        Initialize parallel execution strategy.
        
        Args:
            num_workers: Number of parallel workers (None for auto)
            verbose: Enable verbose output
        """
        super().__init__(verbose)
        self.num_workers = num_workers or self.config.MAX_WORKERS
    
    def build_pytest_args(self) -> List[str]:
        """Build arguments for parallel execution."""
        args = self.config.DEFAULT_ARGS.copy()
        args.extend([
            "-n", str(self.num_workers),  # Number of workers
            "--dist", "loadgroup",         # Distribution strategy
        ])
        args.append("tests/")
        return args


class CoverageStrategy(TestExecutionStrategy):
    """Strategy to execute tests with coverage reporting."""
    
    def __init__(self, min_coverage: Optional[float] = None, verbose: bool = True):
        """
        Initialize coverage strategy.
        
        Args:
            min_coverage: Minimum coverage percentage required
            verbose: Enable verbose output
        """
        super().__init__(verbose)
        self.min_coverage = min_coverage or self.config.COVERAGE_MIN_PERCENTAGE
    
    def build_pytest_args(self) -> List[str]:
        """Build arguments with coverage collection."""
        args = self.config.DEFAULT_ARGS.copy()
        args.extend([
            "--cov=app",                              # Coverage for app package
            "--cov-report=term-missing",              # Show missing lines
            "--cov-report=html",                      # HTML report
            f"--cov-fail-under={self.min_coverage}",  # Minimum coverage
        ])
        args.append("tests/")
        return args
