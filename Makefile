SHELL := /bin/bash
WGET := wget -nc -P
POETRY_RUN := poetry run
TRUNCATE ?= --max_rows 10000

csv := core.surface_site_county_state_materialized_view.zip
url_data := http://geothermal.smu.edu/static/DatasetsZipped8072020/$(csv)
docker_image := altair_demo
docker_container := app

.PHONY: all
all: clean create-db deploy

# Virtual environments
.make.install.prod: poetry.lock
	poetry install --no-dev
	rm -f .make.install.*
	touch $@

.make.install.dev: poetry.lock
	poetry install
	rm -f .make.install.*
	touch $@

.PHONY: install
install: .make.install.prod

.PHONY: install-dev
install-dev: .make.install.dev

# Package managements
poetry.lock: pyproject.toml
	poetry lock
	touch $@

requirements.txt: poetry.lock
	poetry export --without-hashes -f requirements.txt -o $@

# Deployment
.PHONY: deploy
deploy: | .make.install.dev
	$(POETRY_RUN) bin/run_app dev

# Database
data:
	mkdir -p $@

data/$(csv): | data
	$(WGET) $| $(url_data)
	touch $@

.PHONY: create-db
create-db: data/$(csv) | .make.install.prod
	bin/init_db
	$(POETRY_RUN) bin/create_table.py $(TRUNCATE) $^

# Testing
tests: test-lint test-unit test-docker

test-lint: | .make.install.dev
	$(POETRY_RUN) flake8 app tests

test-unit: | .make.install.dev
	$(POETRY_RUN) pytest --cov=app -s

test-docker:
	tests/test_docker

# Docker
.PHONY: docker-image
docker-image:
	docker build -t $(docker_image) .

.PHONY: docker-run
docker-run: docker-image
	docker run --rm -d --name $(docker_container) $(docker_image)

.PHONY: docker-stop
docker-stop:
	docker container stop $(docker_container)

.PHONY: docker-shell
docker-shell:
	docker exec -it $(docker_container) bash

# Utility
.PHONY: clean
clean:
	rm -f .make.*
	rm -rf data
	poetry env remove $$(poetry env list | grep -oP "^\S+")
	find . | grep __pycache__ | xargs rm -rf
