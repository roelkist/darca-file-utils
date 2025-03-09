.PHONY: all format lint test security check

# Default target: run tests
all: test

# Auto-format code using Black and isort using tox
format:
	tox -e format

# Linting using flake8, black, and isort via tox
lint:
	tox -e lint

# Run tests with pytest inside tox environments
test:
	tox -r

# Run all checks before pushing code (format, lint, test, security)
check: format lint test security