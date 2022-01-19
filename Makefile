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
.make.install: poetry.lock
	poetry install
	touch $@

.PHONY: install
install: .make.install

poetry.lock: pyproject.toml
	poetry lock
	touch $@

requirements.txt: poetry.lock
	poetry export --without-hashes -f requirements.txt -o $@

# Deployment
.PHONY: deploy
deploy: | .make.install
	$(POETRY_RUN) bin/run_app

# Database
data:
	mkdir -p $@

data/$(csv): | data
	$(WGET) $| $(url_data)
	touch $@

.PHONY: create-db
create-db: data/$(csv) | .make.install
	bin/init_db
	$(POETRY_RUN) bin/create_table.py $(TRUNCATE) $^

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
	rm -rf data
	poetry env remove $$(poetry env list | grep -oP "^\S+")
	find . | grep __pycache__ | xargs rm -rf
