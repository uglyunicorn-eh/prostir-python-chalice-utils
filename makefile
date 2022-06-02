ENV ?= .env
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VIRTUAL_ENV := ${ROOT_DIR}/${ENV}
SRC=chalice_utils

.PHONY: build package cleanup build_all lint test all docs clean_dist

build:
	python3 setup.py build_ext -t /tmp/ -b build

package:
	python setup.py sdist

cleanup:
	- rm -rf build/
	- rm -rf dist/
	- rm -rf *.egg-info
	- rm -f MANIFEST
	- rm -rf .pytest_cache

build_all: cleanup build

lint:
	@PATH="${VIRTUAL_ENV}/bin" python -m pylint -f colorized --exit-zero ${SRC}

test: lint
	@PATH="${VIRTUAL_ENV}/bin" python -m coverage erase
	@PATH="${VIRTUAL_ENV}/bin" python -m coverage run -m pytest --cov=${SRC} --cov-report term-missing:skip-covered --cov-report xml

all: test build_all package

docs:
	sphinx-apidoc --no-headings --templatedir=docs/templates -f -o docs/source ${SRC}
	$(MAKE) -C docs html
