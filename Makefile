TEST_FILES_STORE :=  test.store_block_test test.store_account_test
TEST_FILE_STORE :=  test.store_transfer_test
TEST_FILES := test.block_handler_test test.transfer_handler_test

.PHONY: test

test:
	python3 -m unittest $(TEST_FILES_STORE)
