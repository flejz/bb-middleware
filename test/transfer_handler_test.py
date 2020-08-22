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
block_transfers_01 = blocks[1]

memory_storage = MemoryStorage()
account_store = AccountStore(memory_storage, "account")
block_store = BlockStore(memory_storage, "block")
transfer_store = TransferStore(memory_storage, "transfer")

transfer_handler = TransferHandler(account_store, transfer_store)
block_handler = BlockHandler(account_store, block_store, transfer_store, transfer_handler)
block_handler.handle_block(block_balances)

initial_balance = account_store.get_balances()

class TestTransferBlock(unittest.TestCase):
    def test_balance_update(self):
        block_handler.handle_block(block_transfers_01)

        for transfer in block_transfers_01["transfers"]:
            transfer_handler.handle_transfer(transfer)

        initial_balance = account_store.get_balances()

    def test_block_added_as_last(self):
        self.assertEqual(get_block_hash(block_transfers_01), block_store.last_hash())

if __name__ == "__main__":
    unittest.main()
