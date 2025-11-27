"""
Quick Test Runner - Run tests with simple commands

Usage:
    python test.py              # Run all tests
    python test.py unit         # Unit tests only
    python test.py fast         # Fast tests (unit only)
    python test.py integration  # Integration tests only
    python test.py coverage     # Run with coverage
    python test.py parallel     # Run in parallel
    python test.py model        # Model layer tests
    python test.py repository   # Repository layer tests
    python test.py service      # Service layer tests
    python test.py help         # Show this help
    python test.py list         # List all available commands
"""
import sys
from tests.test_runner import test_suite

COMMANDS = {
    'all': ('Run all tests', test_suite.run_all_tests),
    'unit': ('Unit tests only', test_suite.run_unit_tests),
    'fast': ('Fast tests (unit only)', test_suite.run_fast),
    'integration': ('Integration tests only', test_suite.run_integration_tests),
    'smoke': ('Smoke tests (critical path)', test_suite.run_smoke),
    'coverage': ('Run with coverage report', test_suite.run_with_coverage),
    'parallel': ('Run tests in parallel', test_suite.run_parallel),
    'model': ('Model layer tests', test_suite.run_model_tests),
    'repository': ('Repository layer tests', test_suite.run_repository_tests),
    'service': ('Service layer tests', test_suite.run_service_tests),
}

def show_help():
    """Display help message."""
    print(__doc__)
    print("\nAvailable Commands:")
    print("-" * 60)
    for cmd, (desc, _) in COMMANDS.items():
        print(f"  {cmd:15} - {desc}")
    print("-" * 60)

def show_list():
    """Show all available test suite commands."""
    test_suite.print_summary()

def main():
    """Execute tests based on command."""
    if len(sys.argv) < 2 or sys.argv[1] == 'all':
        cmd = 'all'
    else:
        cmd = sys.argv[1].lower()
    
    if cmd in ['help', '-h', '--help']:
        show_help()
        return 0
    
    if cmd in ['list', '-l', '--list']:
        show_list()
        return 0
    
    if cmd not in COMMANDS:
        print(f"❌ Unknown command: {cmd}")
        print(f"Run 'python test.py help' for usage")
        return 1
    
    desc, func = COMMANDS[cmd]
    print(f"🚀 {desc}...\n")
    exit_code = func()
    
    print()
    if exit_code == 0:
        print("✅ Tests passed!")
    else:
        print(f"❌ Tests failed (exit code: {exit_code})")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
