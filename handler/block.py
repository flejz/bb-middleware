from store import AccountStore, BlockStore
from handler.transfer import TransferHandler

class BlockHandler():
    def __init__(self, account_store, block_store, transfer_store, transfer_handler):
        self.account_store = account_store
        self.block_store = block_store
        self.transfer_store = transfer_store
        self.transfer_handler = transfer_handler

    def handle_account_balances(self, block):
        if "balances" not in block:
            return None

        for address, amount in block["balances"].items():
            self.account_store.set_balance(address, amount)

        return self.account_store.get_balances()

    def handle_transfers(self, block):
        for trasnfer in block["transfers"]:
            self.transfer_handler.handle_transfer(transfer)

        return self.transfer_store.get_transfers(block["hash"])

    def handle_block(self, block):
        self.block_store.add(block)

        transfers = self.handle_transfers(block)
        balances = self.handle_account_balances(block)

        return transfers, balances
