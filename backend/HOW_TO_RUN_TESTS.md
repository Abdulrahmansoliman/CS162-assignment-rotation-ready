# Test Runner Guide

## Quick Start - Run Tests in 2 Simple Ways

### 1. **Simplest** - Use `test.py`
```bash
python test.py              # Run all tests
python test.py unit         # Unit tests only
python test.py fast         # Fast tests
python test.py coverage     # With coverage
python test.py help         # Show all options
```

### 2. **Full Control** - Use `run_tests.py`
```bash
python run_tests.py                  # Run all tests
python run_tests.py --unit           # Unit tests
python run_tests.py --integration    # Integration tests
python run_tests.py --fast           # Fast mode
python run_tests.py --coverage       # With coverage
python run_tests.py --parallel       # Parallel execution
python run_tests.py --help           # Full options
```

---

## Available Test Commands

### Basic Options
- `python test.py` or `python test.py all` - Run all tests
- `python test.py unit` - Unit tests only (fast feedback)
- `python test.py fast` - Same as unit (quick development)
- `python test.py integration` - Integration tests only
- `python test.py smoke` - Critical path tests

### Layer-Specific Tests
- `python test.py model` - Model layer tests
- `python test.py repository` - Repository layer tests
- `python test.py service` - Service layer tests

### Advanced Options
- `python test.py coverage` - Run with coverage report
- `python test.py parallel` - Run tests in parallel (faster)

### Help & Info
- `python test.py help` - Show usage help
- `python test.py list` - List all available commands

---

## Test Results Summary

**Total Tests:** 153
- **Unit Tests:** 94 (models, repositories, services)
- **Integration Tests:** 59 (end-to-end workflows)

**Current Status:** 152 passing, 1 failing

---

## Examples

```bash
# During development - quick feedback
python test.py fast

# Before committing
python test.py unit

# Before pushing
python test.py

# Full verification with coverage
python test.py coverage

# Specific layer testing
python test.py model
python test.py repository
```

---

## Test Architecture

The test runner provides:
- **Unified Interface** - Single entry point with simple methods
- **Flexible Execution** - Run all tests, specific layers, or custom combinations
- **Multiple Modes** - Fast/full, parallel, with coverage, etc.

**Key Files:**
- `test.py` - Simple command interface (recommended for daily use)
- `run_tests.py` - Full CLI with all options (advanced usage)
- `tests/test_suite_facade.py` - Main test runner interface
- `tests/test_execution_strategies.py` - Execution strategies
- `tests/test_suite_config.py` - Configuration and test categories

---

## Need Help?

Run `python test.py help` or `python run_tests.py --help`
