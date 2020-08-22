from store.generic import GenericStore
from storage.factory import StorageType
from model.block import get_block_hash, get_block_height

class BlockStore(GenericStore):
    def init(self):
        self.block = self.storage_factory.branch('block', StorageType.KEY_VALUE)
        self.chain = self.storage_factory.branch('chain', StorageType.LIST)

    def last_hash(self):
        chain = self.get_chain()
        return None if len(chain) == 0 else get_block_hash(chain[len(chain) - 1])

    def get_height(self):
        block_hash = self.last_hash()
        return None if block_hash is None else get_block_height(self.block.get(block_hash))

    def add_block(self, block):
        # updating block
        block_hash = get_block_hash(block)
        if self.block.get(block_hash) != None:
            raise BlockRepeatedException()

        # updating chain
        self.block.update(block_hash, block)
        self.chain.add(block)

    def get_chain(self):
        return self.chain.get_all() or []

class BlockRepeatedException(Exception):
    pass
