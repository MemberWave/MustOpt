SHELL = /bin/bash

.PHONY: all
all: help ;

.PHONY: env
env: venv/pyvenv.cfg venv-lint/pyvenv.cfg;

.PHONY: remove-env
remove-env:
	rm -rf ./venv*

venv/pyvenv.cfg:
	hatch env create

venv-lint/pyvenv.cfg:
	hatch env create lint

.PHONY : format
format: venv-lint/pyvenv.cfg
	hatch env run -e lint fmt

.PHONY: lint
lint: venv-lint/pyvenv.cfg
	hatch env run -e lint all

.PHONY: test
test: venv-lint/pyvenv.cfg
	hatch run test

.PHONY: test-cov
test-cov: venv-lint/pyvenv.cfg
	hatch run cov

.PHONY: help
help:
	@echo 'Available targets:'
	@echo ''
	@echo '# Dev'
	@echo '  - format          -  Format source code'
	@echo '  - lint            -  Check linting'
	@echo '  - test            -  Run tests'
	@echo '  - test-cov        -  Run coverage test'
	@echo '## Env'
	@echo '  - env             -  Create venvs for development and linting'
	@echo '  - remove-env      -  Prune all venvs'
	@echo ''
	@echo '# Misc'
	@echo '  - help            -  Show this message'