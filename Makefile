TESTS = tests

VENV ?= .venv
CODE = tests app

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: venv
venv:
	python3.9 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install


.PHONY: venv-win
venv:
	python3.9 -m venv $(VENV)
	$(VENV)/Scripts/python -m pip install --upgrade pip
	$(VENV)/Scripts/python -m pip install poetry
	$(VENV)/Scripts/poetry install

.PHONY: test
test: ## Runs pytest
	$(VENV)/bin/pytest -v -s tests

.PHONY: lint
lint: ## Lint code
	$(VENV)/bin/flake8 --jobs 4 --statistics --show-source $(CODE)
	$(VENV)/bin/pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(VENV)/bin/mypy $(CODE)
	$(VENV)/bin/black --skip-string-normalization --check $(CODE)

.PHONY: format
format: ## Formats all files
	$(VENV)/bin/isort $(CODE)
	$(VENV)/bin/black --skip-string-normalization $(CODE)
	$(VENV)/bin/autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	$(VENV)/bin/unify --in-place --recursive $(CODE)

.PHONY: ci
ci:	lint test ## Lint code then run tests

.PHONY: up
up:
	uvicorn --factory app.api:create_api --reload

.PHONY: redis
redis:
	redis-server

.PHONY: console
console:
	python3 -m app.clients.console
