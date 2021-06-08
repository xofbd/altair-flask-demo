SHELL := /bin/bash
ACTIVATE_VENV := source venv/bin/activate

.PHONY: all clean deploy

all: clean venv deploy

venv: requirements.txt
	test -d $@ || python3 -m venv $@
	$(ACTIVATE_VENV) && pip install -r $^
	touch $@

.PHONY: deploy
deploy: | venv
	$(ACTIVATE_VENV) && bin/run_app

.PHONY: clean
clean:
	rm -rf venv
	rm -rf data
	find . | grep __pycache__ | xargs rm -rf
