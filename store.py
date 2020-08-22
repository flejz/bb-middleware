class GenericStore:
    def __init__(self, provider, ref):
        self.provider = provider
        self.ref = ref

    def update(self, ref_id, data):
        return self.provider.update(self.ref, ref_id, data)

    def get_all(self):
        return self.provider.get_all(self.ref)

    def get(self, ref_id):
        return self.provider.get(self.ref, ref_id)


class AccountStore(GenericStore):
    def set_balance(self, address, amount):
        self.update(address, amount)

    def transfer(self, from_address, to_address, amount):
        pass

    def get_balances(self):
        return self.get_all()

class EventStore(GenericStore):
    def get_events():
        pass


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
