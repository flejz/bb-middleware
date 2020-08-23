import unittest

from mock.blocks import mock
from handler.account import AccountHandler
from handler.block import BlockHandler, BlockRepeatedException
from storage.factory import StorageFactory
from storage.memory import MemoryStorage
from model.block import *

blocks = mock()
block_subset_h10 = blocks[:10]
block_subset_h15 = blocks[:15]

def get_last_highest(block_subset):
    current_height = -1
    current_heighest_block = None
    for block in block_subset:
        if get_block_height(block) >= current_height:
            current_height = get_block_height(block)
            current_heighest_block = block

    return current_heighest_block

class TestBlockHandler(unittest.TestCase):
    def setUp(self):
        storage_factory = StorageFactory(MemoryStorage)
        account_handler = AccountHandler(storage_factory)
        self.block_handler = BlockHandler(storage_factory, account_handler)

    def test_should_add_non_repeated_blocks(self):
        for block in block_subset_h15:
            self.block_handler.add_block(block)

    def test_should_raise_exception_on_adding_repeated_blocks(self):
        self.block_handler.add_block(block_subset_h15[0])
        with self.assertRaises(BlockRepeatedException):
            self.block_handler.add_block(block_subset_h15[0])

    def test_should_get_proper_block_chain(self):
        block_chain = [
            get_block_hash(block_subset_h15[14]),
            get_block_hash(block_subset_h15[13]),
            get_block_hash(block_subset_h15[12]),
        ]

        for block in block_subset_h15:
            self.block_handler.add_block(block)

        self.assertEqual(self.block_handler.get_block_chain(), block_chain)

    def test_should_get_highest_hash(self):
        for block in block_subset_h15:
            self.block_handler.add_block(block)

        highest_block = get_last_highest(block_subset_h15)
        self.assertEqual(self.block_handler.last_block_hash(), get_block_hash(highest_block))

    def test_should_get_the_chain_height(self):
        for block in block_subset_h15:
            self.block_handler.add_block(block)

        highest_block = get_last_highest(block_subset_h15)
        self.assertEqual(self.block_handler.get_height(), get_block_height(highest_block))

    def test_should_reorder_blocks_accordinly(self):
        reverted_blocks = [
            get_block_hash(block_subset_h10[1]),
            get_block_hash(block_subset_h10[2]),
            get_block_hash(block_subset_h10[3]),
            get_block_hash(block_subset_h10[5]), # 5th reverts before 4th
            get_block_hash(block_subset_h10[4]),
            get_block_hash(block_subset_h10[8]),
        ]
        for block in block_subset_h10:
            self.block_handler.add_block(block)

        self.assertEqual(self.block_handler.get_block_chain_reverted(), reverted_blocks)

    def test_should_navigate_back_to_the_genesis_block(self):
        for block in block_subset_h15:
            self.block_handler.add_block(block)

        reverted_blocks = self.block_handler.get_block_chain_reverted()

        def back_to_genesis(block_hash, chain_count = 1):
            # must not be in the reverted blocks
            self.assertFalse(block_hash in reverted_blocks)
            block = self.block_handler.get_block(block_hash)
            if get_block_height(block) == 0:
                return chain_count

            return back_to_genesis(get_block_prevhash(block), chain_count + 1)

        block_chain_count = back_to_genesis(self.block_handler.last_block_hash())
        self.assertEqual(block_chain_count - 1, self.block_handler.get_height())

if __name__ == "__main__":
    unittest.main()
