.PHONY: test test-unit test-integration test-smoke test-cov test-fast help

help:
	@echo "Test Commands:"
	@echo "  make test              - Run all tests"
	@echo "  make test-unit         - Run unit tests only"
	@echo "  make test-integration  - Run integration tests only"
	@echo "  make test-smoke        - Run smoke tests only"
	@echo "  make test-fast         - Run fast tests (unit, not slow)"
	@echo "  make test-cov          - Run tests with coverage report"

test:
	pytest

test-unit:
	pytest -m "unit"

test-integration:
	pytest -m "integration"

test-smoke:
	pytest -m "smoke"

test-fast:
	pytest -m "unit and not slow"

test-cov:
	pytest --cov=app --cov-report=term-missing --cov-report=html
