from store import AccountStore, BlockStore

class BlockHandler():
    def __init__(self, account_store, block_store):
        self.account_store = account_store
        self.block_store = block_store

    def handle_balances(self, block):
        for address, amount in block["balances"].items():
            self.account_store.set_balance(address, amount)

        return self.account_store.get_balances()

    def handle_events(self, block):
        pass

    def handle_block(self, block):
        self.block_store.add(block)
        events = self.handle_events(block)
        balances = None

        if "balances" in block:
            balances = self.handle_balances(block)

        return events, balances
