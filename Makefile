.PHONY: all reformat tests requirements precommit coverage docs clean

# Default target: run tests.
all: tests

reformat:
	black -l 79 .
	isort -l 79 --profile black .

tests:
	tox -r

requirements:
	pipenv lock
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

precommit:
	pre-commit install
	pre-commit run --all-files --show-diff-on-failure

coverage:
	coverage report
	coverage html -i

docs:
	tox -e docs

clean:
	@echo "Cleaning up temporary files..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
