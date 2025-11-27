"""
Simple test runner - wraps pytest for convenience

Usage:
    python test.py              # Run all tests
    python test.py unit         # Unit tests only
    python test.py integration  # Integration tests only
    python test.py smoke        # Smoke tests only
    python test.py fast         # Fast tests (unit, no slow)
    python test.py cov          # Run with coverage
"""
import sys
import pytest

COMMANDS = {
    'all': [],
    'unit': ['-m', 'unit'],
    'integration': ['-m', 'integration'],
    'smoke': ['-m', 'smoke'],
    'fast': ['-m', 'unit and not slow'],
    'cov': ['--cov=app', '--cov-report=term-missing'],
}

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    if cmd not in COMMANDS:
        print(__doc__)
        print(f"\nError: Unknown command '{cmd}'")
        print(f"Available: {', '.join(COMMANDS.keys())}")
        sys.exit(1)
    
    sys.exit(pytest.main(COMMANDS[cmd]))
