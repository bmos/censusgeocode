# This file is part of censusgeocode.
# https://github.com/fitnr/censusgeocode

# Licensed under the General Public License (version 3)
# http://opensource.org/licenses/LGPL-3.0
# Copyright (c) 2015-2026, Neil Freeman <contact@fakeisthenewreal.org>

PYTHON = python3
PIP = $(PYTHON) -m pip
BUILD = $(PYTHON) -m build
TWINE = $(PYTHON) -m twine

.PHONY: help install dev-install test lint format build upload clean

help:
	@echo "Usage: make [target]"
	@echo "  install      Install the package"
	@echo "  lint         Install and run formatting, linting, and type checks"
	@echo "  test         Install and run unit tests"
	@echo "  build        Create source and wheel distributions"
	@echo "  upload       Upload to PyPI using Twine"
	@echo "  clean        Remove build artifacts and tooling caches"

install:
	$(PIP) install .

test:
	$(PIP) install -e .[lint]
	$(PYTHON) -m ruff format
	$(PYTHON) -m ruff check --fix
	$(PYTHON) -m bandit --confidence-level 'medium' --severity-level 'medium' --recursive 'src'
	$(PYTHON) -m mypy src
	$(PYTHON) -m mypy tests

test:
	$(PIP) install -e .[test]
	$(PYTHON) -m pytest

build: clean
	$(BUILD)

upload: build
	$(TWINE) upload dist/*

clean:
	rm -rf dist/ build/ *.egg-info .*_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
