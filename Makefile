-include .env
export

PROJECT_NAME := tagpatch

.PHONY: run format build test

format:
	black .

run:
	python -m tagpatch

build:
	pex . -r requirements.txt -o ./build/$(PROJECT_NAME) -e $(PROJECT_NAME).__main__:main

test:
	python -m unittest