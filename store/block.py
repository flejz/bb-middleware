from store.generic import GenericStore
from storage.factory import StorageType
from model.block import get_block_hash, get_block_prevhash, get_block_height

class BlockStore(GenericStore):
    def init(self):
        self.block = self.storage_factory.branch('block', StorageType.KEY_VALUE)
        self.chain = self.storage_factory.branch('chain', StorageType.LIST)
        self.chain_reverted = self.storage_factory.branch('chain_reverted', StorageType.LIST)

    def last_hash(self):
        return self.chain.last()

    def get_height(self):
        block_hash = self.last_hash()
        return -1 if block_hash is None else get_block_height(self.block.get(block_hash))

    def revert_up_to(self, block, prev_block_hash):
        if prev_block_hash == None:
            return

        prev_block = self.block.get(prev_block_hash)
        if get_block_height(prev_block) >= get_block_height(block):
            self.chain_reverted.add(prev_block_hash)
            self.revert_up_to(block, get_block_prevhash(prev_block))

    def add_block(self, block):
        block_hash = get_block_hash(block)
        if self.block.get(block_hash) != None:
            raise BlockRepeatedException()

        # revert on reorder
        self.revert_up_to(block, self.chain.last())

        # updating chain
        self.block.update(block_hash, block)
        self.chain.add(block_hash)

    def get_chain(self):
        return self.chain.get_all() or []

class BlockRepeatedException(Exception):
    pass
