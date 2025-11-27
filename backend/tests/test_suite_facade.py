"""
Test Suite Facade

Provides a unified interface for running tests with different configurations.
"""
from typing import List, Optional

from tests.test_suite_config import TestCategory, TestLevel
from tests.test_execution_strategies import (
    TestExecutionStrategy,
    AllTestsStrategy,
    UnitTestsStrategy,
    IntegrationTestsStrategy,
    CategoryBasedStrategy,
    LevelBasedStrategy,
    ParallelExecutionStrategy,
    CoverageStrategy
)


class TestSuiteFacade:
    """
    Unified interface for running tests with different configurations.
    
    Simplifies test execution by providing convenient methods that handle
    pytest argument construction and execution internally.
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the test suite facade.
        
        Args:
            verbose: Enable verbose output during test execution
        """
        self.verbose = verbose
    
    def run_all_tests(self) -> int:
        """
        Run all tests in the suite (unit + integration).
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        strategy = AllTestsStrategy(verbose=self.verbose)
        return strategy.execute()
    
    def run_unit_tests(self) -> int:
        """
        Run only unit tests.
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        strategy = UnitTestsStrategy(verbose=self.verbose)
        return strategy.execute()
    
    def run_integration_tests(self) -> int:
        """
        Run only integration tests.
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        strategy = IntegrationTestsStrategy(verbose=self.verbose)
        return strategy.execute()
    
    def run_by_category(self, categories: List[TestCategory]) -> int:
        """
        Run tests filtered by specific categories.
        
        Args:
            categories: List of test categories to run
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        strategy = CategoryBasedStrategy(categories, verbose=self.verbose)
        return strategy.execute()
    
    def run_by_level(self, level: TestLevel) -> int:
        """
        Run tests based on execution level.
        
        Args:
            level: Test execution level (FAST, MEDIUM, FULL, SMOKE)
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        strategy = LevelBasedStrategy(level, verbose=self.verbose)
        return strategy.execute()
    
    def run_with_coverage(self, min_coverage: float = 80.0) -> int:
        """
        Run all tests with coverage reporting.
        
        Args:
            min_coverage: Minimum coverage percentage required
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        strategy = CoverageStrategy(min_coverage, verbose=self.verbose)
        return strategy.execute()
    
    def run_parallel(self, num_workers: Optional[int] = None) -> int:
        """
        Run all tests in parallel.
        
        Args:
            num_workers: Number of parallel workers (None for auto-detect)
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        strategy = ParallelExecutionStrategy(num_workers, verbose=self.verbose)
        return strategy.execute()
    
    def run_fast(self) -> int:
        """
        Run fast tests only (unit tests).
        
        Convenience method for quick feedback during development.
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        return self.run_by_level(TestLevel.FAST)
    
    def run_smoke(self) -> int:
        """
        Run smoke tests only.
        
        Convenience method for critical path validation.
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        return self.run_by_level(TestLevel.SMOKE)
    
    def run_repository_tests(self) -> int:
        """
        Run only repository layer tests.
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        return self.run_by_category([TestCategory.REPOSITORY])
    
    def run_service_tests(self) -> int:
        """
        Run only service layer tests.
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        return self.run_by_category([TestCategory.SERVICE])
    
    def run_model_tests(self) -> int:
        """
        Run only model tests.
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        return self.run_by_category([TestCategory.MODEL])
    
    def print_summary(self):
        """Print a summary of available test commands."""
        summary = """
╔══════════════════════════════════════════════════════════════════════╗
║                        TEST SUITE COMMANDS                           ║
╠══════════════════════════════════════════════════════════════════════╣
║ Quick Commands:                                                      ║
║   run_all_tests()          - Run all unit + integration tests       ║
║   run_unit_tests()         - Run only unit tests                    ║
║   run_integration_tests()  - Run only integration tests             ║
║   run_fast()               - Run fast tests (unit only)             ║
║   run_smoke()              - Run smoke tests (critical path)        ║
║                                                                      ║
║ Layer-Specific:                                                      ║
║   run_model_tests()        - Run model layer tests                  ║
║   run_repository_tests()   - Run repository layer tests             ║
║   run_service_tests()      - Run service layer tests                ║
║                                                                      ║
║ Advanced:                                                            ║
║   run_with_coverage()      - Run with coverage report               ║
║   run_parallel()           - Run tests in parallel                  ║
║   run_by_level(level)      - Run by TestLevel (FAST/MEDIUM/FULL)   ║
║   run_by_category(cats)    - Run specific test categories           ║
╚══════════════════════════════════════════════════════════════════════╝
        """
        print(summary)


# Global instance for convenient access
# This is a module-level instance, not a Singleton pattern
test_suite = TestSuiteFacade()
