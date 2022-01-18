SHELL := /bin/bash
WGET := wget -nc -P
VENV := venv
ACTIVATE_VENV := source $(VENV)/bin/activate
TRUNCATE ?= --max_rows 10000

csv := core.surface_site_county_state_materialized_view.zip
url_data := http://geothermal.smu.edu/static/DatasetsZipped8072020/$(csv)
docker_image := altair_demo
docker_container := app

.PHONY: all
all: clean create-db deploy

$(VENV): requirements.txt
	rm -rf $@
	python3 -m venv $@
	$(ACTIVATE_VENV) && pip install -r $<
	touch $@

.PHONY: deploy
deploy: | $(VENV)
	$(ACTIVATE_VENV) && bin/run_app

data:
	mkdir -p $@

data/$(csv): | data
	$(WGET) $| $(url_data)
	touch $@

.PHONY: create-db
create-db: data/$(csv) | $(VENV)
	bin/init_db
	$(ACTIVATE_VENV) && bin/create_table.py $(TRUNCATE) $^

.PHONY: clean
clean:
	rm -rf $(VENV)
	rm -rf data
	find . | grep __pycache__ | xargs rm -rf

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
