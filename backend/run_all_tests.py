"""
Run All Tests

Simple entry point to execute the complete test suite.
Just run: python run_all_tests.py
"""
import sys
from tests.test_suite_facade import test_suite


def main():
    """Execute all tests and return appropriate exit code."""
    print("=" * 70)
    print("🚀 Running Complete Test Suite (Unit + Integration)")
    print("=" * 70)
    print()
    
    exit_code = test_suite.run_all_tests()
    
    print()
    print("=" * 70)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Tests failed with exit code: {exit_code}")
    print("=" * 70)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
