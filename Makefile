TEST_FILES := test.handler_block_test test.handler_account_test

.PHONY: test

test:
	python3 -m unittest $(TEST_FILES)

install:
	.venv/bin/pip3 install -r requirements.txt

run-rest-server:
	FLASK_APP=api/rest/server.py .venv/bin/flask run

run-event-listener:
	echo "TODO"

setup-virtualenv:
	pip3 install virtualenv
	virtualenv .venv

setup: setup-virtualenv install

setup-and-run-rest-server: setup run-rest-server

setup-and-run-event-listener: setup run-event-listener
