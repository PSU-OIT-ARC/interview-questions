.PHONY: print-env \
        initial-setup \
        install \
        install-update \
        install-package \
        virtualenv \
        clean \
        recreate-db \
        manage \
        run \
        shell \
        test \
        coverage \
        reload \

.DEFAULT_GOAL := run

PROJECT_NAME = iq
VENV_DIR ?= .env
BIN_DIR = $(VENV_DIR)/bin
PYTHON = $(BIN_DIR)/python
PIP = $(BIN_DIR)/pip
MANAGE = $(PYTHON) manage.py

print-env:
	@echo PROJECT_NAME: $(PROJECT_NAME)
	@echo VENV_DIR: $(VENV_DIR)
	@echo BIN_DIR: $(BIN_DIR)
	@echo PYTHON: $(PYTHON)
	@echo PIP: $(PIP)
	@echo MANAGE: $(MANAGE)

initial-setup: virtualenv
	cp $(PROJECT_NAME)/settings/local.py.template $(PROJECT_NAME)/settings/local.py
	mysql -u root -e 'create database $(PROJECT_NAME);'
	$(MANAGE) syncdb
	$(MANAGE) migrate
	$(MANAGE) test

install:
	$(PIP) install -r requirements.txt

install-update:
	$(PIP) install -U -r requirements.txt

# pip install $(args)
# Examples:
#     make install-package args=bpython
#     make install-package args='pep8 pyflakes'
#     make install-package args='-U pep8'
install-package:
	$(PIP) install $(args)

virtualenv:
	@if [ -d "$(VENV_DIR)" ]; then \
	    echo "Directory exists: $(VENV_DIR)"; \
	    exit 1; \
	fi
	virtualenv --no-site-packages $(VENV_DIR)
	@echo
	$(MAKE) install

# remove pyc junk
clean:
	find . -iname "*.pyc" -delete
	find . -iname "*.swp" -delete
	find . -iname "*~" -delete
	find . -iname "__pycache__" -delete

recreate-db:
	mysql -u root -e 'drop database $(PROJECT_NAME);' || true
	mysql -u root -e 'create database $(PROJECT_NAME);'
	$(MANAGE) syncdb
	$(MANAGE) migrate

## Django (wrappers for ./manage.py commands)

# Run a manage.py command
#
# This is here so we don't have to create a target for every single manage.py
# command. Of course, you could also just source your virtualenv's bin/activate
# script and run manage.py directly, but this provides consistency if you're in
# the habit of using make.
#
# Examples:
#     make manage args=migrate
#     make manage args='runserver 8080'
manage:
	@$(MANAGE) $(args)

# run the django web server
host ?= 0.0.0.0
port ?= 8000
run:
	$(MANAGE) runserver $(host):$(port)

# start a django shell
# run `make install-package name=bpython` (or ipython) first if you want
# a fancy shell
shell:
	$(MANAGE) shell $(args)

# run the unit tests
# use `make test test=path.to.test` if you want to run a specific test
test:
	$(MANAGE) test $(test)

# run the unit tests using coverage
coverage:
	coverage run $(MANAGE) test && coverage html

reload:
	$(MANAGE) migrate && \
		$(MANAGE) collectstatic --noinput && \
		touch $(PROJECT_NAME)/wsgi.py

## /Django
