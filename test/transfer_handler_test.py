import unittest

from mock.blocks import mock
from provider import MemoryProvider
from store import *
from handler.block import BlockHandler
from handler.tranfer import TranferHandler

blocks = mock()[:2]
block_balances = blocks[0]
block_transfers_01 = blocks[1]

memory_provider = MemoryProvider()
account_store = AccountStore(memory_provider, "account")
block_store = BlockStore(memory_provider, "block")

transfer_handler = TransferHandler()

block_handler = BlockHandler(account_store, block_store)
block_handler.handle_block(block_balances)

initial_balance = account_store.get_balances()

class TestBalanceBlock(unittest.TestCase):
    def test_balance_update(self):
        block_handler.handle_block(block_transfers_01j)

        for transfer in block_transfers_01["transfers"]:
            transfer_handler.handle_transfer(transfer)

        initial_balance = account_store.get_balances()

    def test_block_added_as_last(self):
        self.assertEqual(block_balances["hash"], block_store.last_hash())

if __name__ == "__main__":
    unittest.main()
