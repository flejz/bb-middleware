import unittest

from mock.blocks import mock
from provider import MemoryProvider
from store import AccountStore
from block_handler import BlockHandler

blocks = mock()
block_balances = blocks[0]

memory_provider = MemoryProvider()
account_store = AccountStore(memory_provider, "account")
block_handler = BlockHandler(account_store)

class TestEventHandler(unittest.TestCase):
    def test_handle_balance_block(self):
        block_handler.handle_block(block_balances)
        self.assertEqual(block_balances["balances"], account_store.get_balances())


if __name__ == "__main__":
    unittest.main()
