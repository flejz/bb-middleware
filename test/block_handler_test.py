import unittest

from mock.blocks import mock
from handler.block import BlockHandler
from handler.transfer import TransferHandler
from storage.memory import MemoryStorage
from store.account import AccountStore
from store.block import BlockStore
from store.transfer import TransferStore
from model.block import get_block_hash

blocks = mock()
block_balances = blocks[0]

memory_storage = MemoryStorage()
account_store = AccountStore(memory_storage, "account")
block_store = BlockStore(memory_storage, "block")
transfer_store = TransferStore(memory_storage, "transfer")

transfer_handler = TransferHandler(account_store, transfer_store)
block_handler = BlockHandler(account_store, block_store, transfer_store, transfer_handler)
block_handler.handle_block(block_balances)

class TestBalanceBlock(unittest.TestCase):
    def test_handler(self):
        self.assertEqual(block_balances["balances"], account_store.get_balances())

    def test_block_added_as_last(self):
        self.assertEqual(get_block_hash(block_balances), block_store.last_hash())

if __name__ == "__main__":
    unittest.main()
