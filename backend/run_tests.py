#!/usr/bin/env python
"""
Test Runner - Main Entry Point

This is the single entry point for running all tests in the application.
Execute this file to run the complete test suite with various options.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run unit tests only
    python run_tests.py --integration      # Run integration tests only
    python run_tests.py --fast             # Run fast tests (unit only)
    python run_tests.py --coverage         # Run with coverage
    python run_tests.py --parallel         # Run tests in parallel
    python run_tests.py --smoke            # Run smoke tests only
    python run_tests.py --model            # Run model tests only
    python run_tests.py --repository       # Run repository tests only
    python run_tests.py --service          # Run service tests only
"""
import sys
import argparse
from pathlib import Path

# Add parent directory to path to import test modules
sys.path.insert(0, str(Path(__file__).parent))

from tests.test_runner import test_suite
from tests.test_suite_config import TestLevel


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Run test suite with various options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      Run all tests
  %(prog)s --unit               Run only unit tests
  %(prog)s --integration        Run only integration tests
  %(prog)s --fast               Run fast tests (for quick feedback)
  %(prog)s --coverage           Run with coverage report
  %(prog)s --parallel           Run tests in parallel
  %(prog)s --model              Run model layer tests
  %(prog)s --repository         Run repository layer tests
  %(prog)s --service            Run service layer tests
  %(prog)s --smoke              Run critical smoke tests

Test Levels:
  --fast        : Only unit tests (fastest)
  --medium      : Unit + integration tests (excludes slow)
  --full        : All tests including slow tests
  --smoke       : Only critical path tests
        """
    )
    
    # Test scope options
    scope_group = parser.add_mutually_exclusive_group()
    scope_group.add_argument(
        "--all",
        action="store_true",
        help="Run all tests (default)"
    )
    scope_group.add_argument(
        "--unit",
        action="store_true",
        help="Run only unit tests"
    )
    scope_group.add_argument(
        "--integration",
        action="store_true",
        help="Run only integration tests"
    )
    
    # Test level options
    level_group = parser.add_mutually_exclusive_group()
    level_group.add_argument(
        "--fast",
        action="store_true",
        help="Run fast tests only (unit tests)"
    )
    level_group.add_argument(
        "--medium",
        action="store_true",
        help="Run medium-speed tests (unit + integration, no slow tests)"
    )
    level_group.add_argument(
        "--full",
        action="store_true",
        help="Run full test suite including slow tests"
    )
    level_group.add_argument(
        "--smoke",
        action="store_true",
        help="Run smoke tests only (critical path)"
    )
    
    # Layer-specific options
    layer_group = parser.add_mutually_exclusive_group()
    layer_group.add_argument(
        "--model",
        action="store_true",
        help="Run model layer tests only"
    )
    layer_group.add_argument(
        "--repository",
        action="store_true",
        help="Run repository layer tests only"
    )
    layer_group.add_argument(
        "--service",
        action="store_true",
        help="Run service layer tests only"
    )
    
    # Execution options
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run tests with coverage reporting"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel (faster execution)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        metavar="N",
        help="Number of parallel workers (default: auto-detect)"
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Quiet mode (less verbose output)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available test commands and exit"
    )
    
    return parser


def main():
    """Main entry point for the test runner."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Set verbosity
    verbose = not args.quiet
    test_suite.verbose = verbose
    
    # List commands and exit if requested
    if args.list:
        test_suite.print_summary()
        return 0
    
    # Determine which tests to run
    exit_code = 0
    
    try:
        if args.coverage:
            # Run with coverage
            print("\n🔬 Running tests with coverage analysis...\n")
            exit_code = test_suite.run_with_coverage()
        
        elif args.parallel:
            # Run in parallel
            print(f"\n⚡ Running tests in parallel (workers: {args.workers or 'auto'})...\n")
            exit_code = test_suite.run_parallel(args.workers)
        
        elif args.fast:
            # Fast tests
            print("\n🚀 Running fast tests (unit only)...\n")
            exit_code = test_suite.run_fast()
        
        elif args.medium:
            # Medium-speed tests
            print("\n⚡ Running medium-speed tests...\n")
            exit_code = test_suite.run_by_level(TestLevel.MEDIUM)
        
        elif args.full:
            # Full test suite
            print("\n🎯 Running full test suite...\n")
            exit_code = test_suite.run_by_level(TestLevel.FULL)
        
        elif args.smoke:
            # Smoke tests
            print("\n💨 Running smoke tests...\n")
            exit_code = test_suite.run_smoke()
        
        elif args.unit:
            # Unit tests only
            print("\n🧪 Running unit tests...\n")
            exit_code = test_suite.run_unit_tests()
        
        elif args.integration:
            # Integration tests only
            print("\n🔗 Running integration tests...\n")
            exit_code = test_suite.run_integration_tests()
        
        elif args.model:
            # Model tests
            print("\n📊 Running model layer tests...\n")
            exit_code = test_suite.run_model_tests()
        
        elif args.repository:
            # Repository tests
            print("\n💾 Running repository layer tests...\n")
            exit_code = test_suite.run_repository_tests()
        
        elif args.service:
            # Service tests
            print("\n⚙️  Running service layer tests...\n")
            exit_code = test_suite.run_service_tests()
        
        else:
            # Default: run all tests
            print("\n✨ Running all tests...\n")
            exit_code = test_suite.run_all_tests()
        
        # Print result
        if exit_code == 0:
            print("\n✅ All tests passed!\n")
        else:
            print(f"\n❌ Tests failed with exit code: {exit_code}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user\n")
        exit_code = 130  # Standard exit code for SIGINT
    except Exception as e:
        print(f"\n\n❌ Error running tests: {e}\n")
        exit_code = 1
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())


