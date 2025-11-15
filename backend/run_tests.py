"""
Test runner for the application
Run all tests: python run_tests.py
Run model tests only: python run_tests.py models
"""
import unittest
import sys

# Discover and run all tests
if __name__ == '__main__':
    loader = unittest.TestLoader()
    
    # Check if specific test suite is requested
    if len(sys.argv) > 1 and sys.argv[1] == 'models':
        start_dir = 'tests/models'
        print("Running model tests only...")
    else:
        start_dir = 'tests'
        print("Running all tests...")
    
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with proper code
    sys.exit(not result.wasSuccessful())

