SHELL:=/bin/bash

.PHONY: all deploy remove_venv

all: venv deploy

venv: requirements.txt
	test -d venv || python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	touch venv

deploy: venv
	source venv/bin/activate && bin/run_app

remove_venv:
	rm -rf venv
