SHELL:=/bin/bash

.PHONY: all clean deploy

all: clean venv deploy

venv: requirements.txt
	test -d venv || python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	touch venv

deploy: venv
	source venv/bin/activate && bin/run_app

clean:
	rm -rf venv
	find . | grep __pycache__ | xargs rm -rf
