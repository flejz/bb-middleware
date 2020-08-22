from store.generic import GenericStore
from model.block import get_block_hash, get_block_height

class BlockStore(GenericStore):
    def last_hash(self):
        chain = self.get_chain()
        return None if len(chain) == 0 else get_block_hash(chain[len(chain) - 1])

    def get_height(self):
        block_hash = self.last_hash()
        return None if block_hash is None else get_block_height(self.get(block_hash))

    def add_block(self, block):
        block_hash = get_block_hash(block)
        if self.get(block_hash) != None:
            raise BlockRepeatedException()

        chain = self.get_chain()
        self.update(block_hash, block)
        return self.update("chain", chain + [block])

    def get_chain(self):
        return self.get("chain") or []

class BlockRepeatedException(Exception):
    pass
