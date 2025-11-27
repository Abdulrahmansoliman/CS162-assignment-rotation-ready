# Running Tests

This project uses pytest for testing. Tests are organized by markers for easy filtering.

## Quick Start

```bash
# Run all tests
pytest

# Or use the convenience script
python test.py
```

## Running Specific Test Types

```bash
# Unit tests only
pytest -m "unit"
python test.py unit

# Integration tests only
pytest -m "integration"
python test.py integration

# Smoke tests (critical path)
pytest -m "smoke"
python test.py smoke

# Fast tests (unit, excluding slow)
pytest -m "unit and not slow"
python test.py fast
```

## With Coverage

```bash
# Coverage report
pytest --cov=app --cov-report=term-missing --cov-report=html
python test.py cov

# View HTML report
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
```

## Using Make (if available)

```bash
make test              # All tests
make test-unit         # Unit tests
make test-integration  # Integration tests
make test-smoke        # Smoke tests
make test-fast         # Fast tests
make test-cov          # With coverage
make help              # Show all commands
```

## Test Markers

Tests are marked with these markers (configured in `pytest.ini`):

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.smoke` - Critical smoke tests
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.model` - Model layer tests
- `@pytest.mark.repository` - Repository layer tests
- `@pytest.mark.service` - Service layer tests
- `@pytest.mark.api` - API endpoint tests
- `@pytest.mark.auth` - Authentication tests

## Combining Markers

```bash
# Unit OR integration
pytest -m "unit or integration"

# Unit AND authentication tests
pytest -m "unit and auth"

# Unit tests but NOT slow ones
pytest -m "unit and not slow"

# Service layer integration tests
pytest -m "service and integration"
```

## Configuration

All pytest configuration is in `pytest.ini`. Default options include:
- Verbose output (`-v`)
- Short traceback (`--tb=short`)
- Strict markers (fail on unknown markers)
- Warnings disabled

## CI Integration

In CI, you can run:

```bash
# Fast feedback
pytest -m "unit and not slow"

# Full suite
pytest

# With coverage threshold
pytest --cov=app --cov-fail-under=80
```
