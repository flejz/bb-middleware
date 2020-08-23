import unittest

from mock.blocks import mock
from handler.block import BlockHandler, BlockRepeatedException
from storage.factory import StorageFactory
from storage.memory import MemoryStorage
from model.block import get_block_hash, get_block_height

blocks = mock()
block_subset_h10 = blocks[:10]
block_subset_h11 = blocks[:11]

def get_last(block_subset):
    return block_subset[len(block_subset) - 1]

class TestBlockHandler(unittest.TestCase):
    def setUp(self):
        self.block_handler = BlockHandler(StorageFactory(MemoryStorage))

    def test_should_add_non_repeated_blocks(self):
        for block in block_subset_h10:
            self.block_handler.add_block(block)

    def test_should_raise_exception_on_adding_repeated_blocks(self):
        self.block_handler.add_block(block_subset_h10[0])
        with self.assertRaises(BlockRepeatedException):
            self.block_handler.add_block(block_subset_h10[0])

    def test_should_get_chain_identical_to_block_subset_h10(self):
        chain = []
        for block in block_subset_h10:
            self.block_handler.add_block(block)
            chain.append(get_block_hash(block))

        self.assertEqual(self.block_handler.get_chain(), chain)

    # TODO: must be fixed given the reorder
    def test_should_get_the_last_hash(self):
        for block in block_subset_h10:
            self.block_handler.add_block(block)

        self.assertEqual(self.block_handler.last_hash(), get_block_hash(get_last(block_subset_h10)))

    # TODO: must be fixed given the reorder
    def test_should_get_the_last_height(self):
        for block in block_subset_h11:
            self.block_handler.add_block(block)

        self.assertEqual(self.block_handler.get_height(), 1)

    # TODO: add reorder test

if __name__ == "__main__":
    unittest.main()
