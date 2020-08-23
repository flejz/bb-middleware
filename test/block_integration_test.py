import unittest
import statistics

from mock.blocks import mock
from handler.account import AccountHandler
from handler.block import BlockHandler, BlockRepeatedException
from storage.factory import StorageFactory
from storage.memory import MemoryStorage
from model.block import *
from model.account import *

blocks = mock()
block_subset_h02 = blocks[:2]
block_subset_h10 = blocks[:10]

class TestBlock(unittest.TestCase):
    def setUp(self):
        storage_factory = StorageFactory(MemoryStorage)
        self.account_handler = AccountHandler(storage_factory)
        self.block_handler = BlockHandler(storage_factory, self.account_handler)

    def test_balance_after_a_block_added(self):
        accounts = {}
        for block in block_subset_h02:
            self.block_handler.add_block(block)

            if "balances" in block:
                for address, amount in get_block_balances(block).items():
                    accounts[address] = amount

            if "transfers" in block:
                for transfer in get_block_transfers(block):
                    amount = get_amount(transfer)

                    accounts[get_sender(transfer)] -= amount
                    accounts[get_receiver(transfer)] += amount

        self.assertEqual(self.account_handler.get_balances(), accounts)

    def test_median_after_a_block_added(self):
        accounts = {}
        for block in block_subset_h02:
            self.block_handler.add_block(block)

            if "balances" in block_subset_h02:
                for address in get_block_balances(block).keys():
                    accounts[address] = []

            if "transfers" in block_subset_h02:
                for transfer in get_block_transfers(block):
                    amount = get_amount(transfer)

                    accounts[get_sender(transfer)].append(amount * -1)
                    accounts[get_receiver(transfer)].append(amount)

        medians = self.account_handler.get_medians()
        for key, values in accounts.items():
            self.assertEqual(medians[key], statistics.median(values))

if __name__ == "__main__":
    unittest.main()
