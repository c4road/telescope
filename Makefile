.PHONY: install build run migrate makemigrations import_companies get_companies process_companies

install:
	pip install -r requirements.txt

build:
	docker build -t telescope . --no-cache

run:
	docker-compose up

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

import_companies:
	chmod +x ./bin/import_companies.sh
	./bin/import_companies.sh

get_companies:
	chmod +x ./bin/get_companies.sh
	./bin/get_companies.sh

process_companies:
	chmod +x ./bin/process_company.sh
	./bin/process_company.sh

run_tests:
	pytest

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

build-package: clean
	@echo "Building version $(VERSION)"
	VERSION=$(VERSION) python setup.py bdist_wheel
	python setup.py bdist_wheel --version $(VERSION)
	ls -l dist

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -fr .pytest_cache
