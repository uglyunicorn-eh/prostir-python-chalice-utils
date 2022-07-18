ENV ?= .env
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VIRTUAL_ENV := ${ROOT_DIR}/${ENV}
SRC=prostir
PYTHON_VERSION=3.9

.PHONY: build package cleanup build_all lint test all docs clean_dist bootstrap

bootstrap: ${ENV} .git/hooks/pre-commit

${ENV}:
	virtualenv -p python${PYTHON_VERSION} --system-site-packages $@
	export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain $(AWS_CODEARTIFACTS_DOMAIN) --domain-owner $(AWS_CODEARTIFACTS_DOMAIN_OWNER) --query authorizationToken --output text --profie $(PROFILE)`
	$(PYTHON) -m pip config set global.extra-index-url https://aws:$(CODEARTIFACT_AUTH_TOKEN)@$(AWS_CODEARTIFACTS_DOMAIN)-$(AWS_CODEARTIFACTS_DOMAIN_OWNER).d.codeartifact.us-west-2.amazonaws.com/pypi/$(AWS_CODEARTIFACTS_REPOSITORY)/simple/ --site
	@PATH="${VIRTUAL_ENV}/bin" python -m pip install -U pip
	@PATH="${VIRTUAL_ENV}/bin" python -m pip install -e ".[develop]"
	@PATH="${VIRTUAL_ENV}/bin" python -m pip install -e ".[docs]"
	@PATH="${VIRTUAL_ENV}/bin" python -m pip install --ignore-installed pylint

.git/hooks/pre-commit:
	pre-commit install

build:
	@PATH="${VIRTUAL_ENV}/bin" python3 setup.py build_ext -t /tmp/ -b build

package: build
	@PATH="${VIRTUAL_ENV}/bin" python setup.py sdist

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

test-only:
	@PATH="${VIRTUAL_ENV}/bin" python -m pytest

all: cleanup test docs build_all package

docs:
	@PATH="${VIRTUAL_ENV}/bin" sphinx-apidoc --force --no-headings --templatedir=docs/templates -f -o docs/source ${SRC}
	@SPHINXBUILD="${VIRTUAL_ENV}/bin/sphinx-build" $(MAKE) -C docs html
