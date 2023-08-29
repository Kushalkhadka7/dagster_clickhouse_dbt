.PHONY: env
.DEFAULT_GOAL := help

SHELL := /bin/bash
APP_ROOT ?= $(shell 'pwd')

export $(cat .env | xargs)

# Build env for dagster development.
dagster-env:
	@python3 --version
	@pip install virtualenv
	@virtualenv dagster-dbt-env
	@source dagster-dbt-env/bin/activate
	@pip install -e ".[dev]"

# Run dagster in development mode.
dagster-dev:
	@dagster dev

# Display available commands for all targets
help: ## Help
	@echo "Help"
