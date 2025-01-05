-include .env
export

PROJECT_NAME := tagpatch

.PHONY: run format build test

format:
	uv tool run ruff check --select I --fix # fix import
	uv tool run ruff format # format

run:
	python -m tagpatch

lint:
	uv tool run ruff check

mypy:
	mypy ./tagpatch

develop:
	uv venv
	uv sync
	uv pip install -e .

build:
	uv pip compile pyproject.toml > requirements.txt

	# build standalone binary
	uvx pex . -r requirements.txt \
		-o ./build/$(PROJECT_NAME) \
		--python-shebang=/usr/bin/python3 \
		-e $(PROJECT_NAME).__main__:main

	# build python package
	rm -rf dist/
	rm -rf tagpatch.egg-info
	uv build

test:
	python -m unittest

publish: build
	uv publish
