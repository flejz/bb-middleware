import unittest

from mock.blocks import mock
from provider import MemoryProvider
from store import *
from handler.block import BlockHandler
from handler.transfer import TransferHandler

blocks = mock()
block_balances = blocks[0]

memory_provider = MemoryProvider()
account_store = AccountStore(memory_provider, "account")
block_store = BlockStore(memory_provider, "block")
transfer_store = TransferStore(memory_provider, "transfer")

transfer_handler = TransferHandler(account_store, transfer_store)
block_handler = BlockHandler(account_store, block_store, transfer_store, transfer_handler)
block_handler.handle_block(block_balances)

class TestBalanceBlock(unittest.TestCase):
    def test_handler(self):
        self.assertEqual(block_balances["balances"], account_store.get_balances())

    def test_block_added_as_last(self):
        self.assertEqual(block_balances["hash"], block_store.last_hash())

if __name__ == "__main__":
    unittest.main()
