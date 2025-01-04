-include .env
export

PROJECT_NAME := tagpatch

.PHONY: run format build test

format:
	uv tool run ruff check --select I --fix # fix import
	uv tool run ruff format # format

run:
	python -m tagpatch

build:
	pex . -r requirements.txt \
		-o ./build/$(PROJECT_NAME) \
		--python-shebang=/usr/bin/python3 \
		-e $(PROJECT_NAME).__main__:main

test:
	python -m unittest

publish:
	rm -rf dist/
	rm -rf tagpatch.egg-info
	pip-compile pyproject.toml
	python -m build
	twine check dist/*
	twine upload dist/*
