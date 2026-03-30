"""
.PHONY: test test-cov test-watch install-test

install-test:
	pip install -r requirements-test.txt

test:
	pytest -v

test-cov:
	pytest --cov=. --cov-report=html --cov-report=term

test-watch:
	pytest-watch

test-fast:
	pytest -x --ff

test-specific:
	pytest tests/test_turn_router.py -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf htmlcov
	rm -f .coverage
"""