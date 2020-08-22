from provider import GenericProvider

class GenericStore:
    def __init__(self, provider: GenericProvider, ref: str):
        self.provider = provider
        self.ref = ref

    def update(self, ref_id, data):
        self.provider.update(self.ref, ref_id, data)

    def get_all(self):
        return self.provider.get_all(self.ref)


class AccountStore(GenericStore):
    def set_balance(self, address, amount):
        self.update(address, amount)

    def get_balances(self):
        return self.get_all()
