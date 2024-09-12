# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help
FILE=VERSION
VERSION=`cat $(FILE)`
COMMIT_MSG_HOOK = '\#!/bin/bash\nMSG_FILE=$$1\ncz check --allow-abort --commit-msg-file $$MSG_FILE'

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo Commands available:
	@echo 	- make install-pip-tools: install pip-tools
	@echo 	- make requirements-dev.txt: create requirements-dev.txt from requirements-dev.in
	@echo 	- make requirements.txt: create requirements.txt from requirements.in
	@echo 	- make install-dev: install development dependencies from requirements-dev.txt
	@echo 	- make install: install dependencies from requirements.txt
	@echo 	- make setup-dev-env: run make install-dev + add git hook for commits syntax checking
	@echo 	- make clean: remove __pycache__ directories and other garbage
	@echo "------------------------------------"


install-pip-tools:
	pip install --upgrade pip
	pip install --upgrade pip-tools

requirements-dev.txt: requirements-dev.in install-pip-tools
	pip-compile --upgrade --resolver backtracking --output-file=$@ requirements-dev.in

requirements.txt: requirements.in install-pip-tools
	pip-compile --upgrade --resolver backtracking --output-file=$@ requirements.in

install-dev: requirements-dev.txt
	pip install  -r requirements-dev.txt

install: requirements.txt
	pip install  -r requirements.txt

setup-dev-env: install-dev
	pre-commit install
	echo $(COMMIT_MSG_HOOK) > .git/hooks/commit-msg
	chmod +x .git/hooks/commit-msg

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} \;
	find . -type d -name .hypothesis -prune -exec rm -rf {} \;
	find . -type d -name .ipynb_checkpoints -prune -exec rm -rf {} \;
	find . -type d -name .pytest_cache -prune -exec rm -rf {} \;
	find . -type d -name .mypy_cache -prune -exec rm -rf {} \;
