TEST_FILES := test.handler_block_test test.handler_account_test

.PHONY: test

test:
	python3 -m unittest $(TEST_FILES)
