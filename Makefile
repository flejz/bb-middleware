TEST_FILES_HANDLER :=  test.handler_block_test test.handler_account_test
TEST_FILES := test.block_handler_test test.transfer_handler_test

.PHONY: test

test:
	python3 -m unittest $(TEST_FILES_HANDLER)
