TEST_FILES := test.handler_block_test test.handler_account_test

.PHONY: test

test:
	python3 -m unittest $(TEST_FILES)

install:
	.venv/bin/pip3 install -r requirements.txt

setup-virtualenv:
	pip3 install virtualenv
	virtualenv .venv

setup: setup-virtualenv install
