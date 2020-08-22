from store.generic import GenericStore

class BlockStore(GenericStore):
    def last_hash(self):
        chain = self.get_chain()
        return None if len(chain) == 0 else chain[len(chain) - 1]["hash"]

    def add(self, block):
        chain = self.get_chain()
        self.update(block["hash"], block)
        return self.update('chain', chain + [block])

    def get_chain(self):
        return self.get('chain') or []

