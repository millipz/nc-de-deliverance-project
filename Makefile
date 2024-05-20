#################################################################################
#
# Makefile to build the project
#
#################################################################################

PROJECT_NAME = de-nc-deliverance-project
REGION = eu-west-2
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PROFILE = default
PIP:=pip

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
		$(PIP) install -q virtualenv virtualenvwrapper; \
		virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install pip-tools)
	$(call execute_in_env, pip-compile requirements.in)
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)
	mkdir layer && cd layer && mkdir python
	cp -r ./venv/lib/python3.11/site-packages/* ./layer/python

################################################################################################################
# Set Up
## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install safety
safety:
	$(call execute_in_env, $(PIP) install safety)

## Install black
black:
	$(call execute_in_env, $(PIP) install black)

## Install coverage
coverage:
	$(call execute_in_env, $(PIP) install coverage)

## Install flake8
flake8:
	$(call execute_in_env, $(PIP) install flake8)

## Set up dev requirements (bandit, safety, black, flake8)
dev-setup: bandit safety black coverage flake8

# Test Database

initialise-test-db:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} $(PYTHON_INTERPRETER) db/run_schema.py)
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} $(PYTHON_INTERPRETER) db/run_seed.py)

run-extract:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} $(PYTHON_INTERPRETER) src/extract.py)

# Build / Run

## Run the security test (bandit + safety)
security-test:
	$(call execute_in_env, safety check -r ./requirements.txt)
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Run the black code formatter
run-black:
	$(call execute_in_env, find . -type f -name "*.py" \
		! -path "./.git/*" ! -path "./__pycache__/*" ! -path "./venv/*" ! -path "./layer/*"\
		! -path "./.github/*" ! -path "./.gitignore/*" ! -path "./.env/*" \
		-exec sed -i '' -e 's/[[:space:]]\+$$//' {} \; \
		-exec black {} \;)

## Run the flake8 code check
run-flake8:
	$(call execute_in_env, flake8 --config .flake8)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -vv --testdox)

## Run the coverage check
check-coverage:
	$(call source venv/bin/activate && find . -path "*/src/*.py" -o -path "*/tests/*.py" -exec pytest --cov=src --cov=tests {} +; PYTHONPATH=${PYTHONPATH})


## Run all checks
run-checks: security-test run-black run-flake8 unit-test check-coverage
