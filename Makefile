SHELL := /bin/bash
WGET := wget -nc -P
ACTIVATE_VENV := source venv/bin/activate

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
	$(ACTIVATE_VENV) && bin/create_table.py $^

.PHONY: clean
clean:
	rm -rf venv
	rm -rf data
	find . | grep __pycache__ | xargs rm -rf
