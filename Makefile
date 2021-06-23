SHELL := /bin/bash
WGET := wget -nc -P
ACTIVATE_VENV := source venv/bin/activate
NUM_ROWS := 10000
DOCKER_IMAGE := altair_demo
DOCKER_CONTAINER := app

csv := core.surface_site_county_state_materialized_view.zip
url_data := http://geothermal.smu.edu/static/DatasetsZipped8072020/$(csv)

.PHONY: all
all: clean create_db deploy

venv: requirements.txt
	test -d $@ || python3 -m venv $@
	$(ACTIVATE_VENV) && pip install -r $^
	touch $@

.PHONY: deploy
deploy: | venv
	$(ACTIVATE_VENV) && bin/run_app

data:
	mkdir -p $@

data/$(csv): | data
	$(WGET) $| $(url_data)
	touch $@

.PHONY: create_db
create_db: data/$(csv) | venv
	bin/init_db
	$(ACTIVATE_VENV) && bin/create_table.py --truncate $(NUM_ROWS) $^

.PHONY: clean
clean:
	rm -rf venv
	rm -rf data
	find . | grep __pycache__ | xargs rm -rf

.PHONY: deploy-docker
deploy-docker: docker-rm
	docker build -t $(DOCKER_IMAGE) .
	docker run -d -p 5000:5000 --name $(DOCKER_CONTAINER) $(DOCKER_IMAGE)

.PHONY: docker-rm
docker-rm:
	-docker rm -f $(DOCKER_CONTAINER)
