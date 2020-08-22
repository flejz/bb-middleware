from store import AccountStore

class BlockHandler():
    def __init__(self, account_store: AccountStore):
        self.account_store = account_store

    def handle_balances(self, block):
        for address, amount in block["balances"].items():
            self.account_store.set_balance(address, amount)

        return self.account_store.get_balances()

    def handle_block(self, block):
        if "balances" in block:
            return self.handle_balances(block)
