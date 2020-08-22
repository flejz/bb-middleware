from store.generic import GenericStore

class AccountStore(GenericStore):
    def set_balance(self, address, amount):
        self.update(address, amount)

    def transfer(self, from_address, to_address, amount):
        pass

    def get_balances(self):
        return self.get_all()
