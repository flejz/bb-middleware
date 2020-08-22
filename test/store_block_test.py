import unittest

from mock.blocks import mock
from storage.memory import MemoryStorage
from store.block import BlockStore, BlockRepeatedException
from model.block import get_block_hash, get_block_height

blocks = mock()
block_subset = blocks[:10]


class TestBlockStore(unittest.TestCase):
    def setUp(self):
        self.block_store = BlockStore(MemoryStorage(), "block")

    def test_should_add_non_repeated_blocks(self):
        for block in block_subset:
            self.block_store.add_block(block)

    def test_should_raise_exception_on_adding_repeated_blocks(self):
        self.block_store.add_block(block_subset[0])
        with self.assertRaises(BlockRepeatedException):
            self.block_store.add_block(block_subset[0])

    def test_should_get_chain_identical_to_block_subset(self):
        for block in block_subset:
            self.block_store.add_block(block)

        self.assertEqual(self.block_store.get_chain(), block_subset)

    # TODO: must be fixed given the reorder
    def test_should_get_the_last_hash(self):
        for block in block_subset:
            self.block_store.add_block(block)

        self.assertEqual(self.block_store.last_hash(), get_block_hash(block_subset[len(block_subset) - 1]))

    # TODO: must be fixed given the reorder
    def test_should_get_the_last_height(self):
        for block in block_subset:
            self.block_store.add_block(block)

        self.assertEqual(self.block_store.get_height(), get_block_height(block_subset[len(block_subset) - 1]))

if __name__ == "__main__":
    unittest.main()