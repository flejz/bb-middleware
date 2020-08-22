from store import AccountStore, TransferStore

class TransferHandler():
    def __init__(self, account_store, transfer_store):
        self.account_store = account_store
        self.transfer_store = transfer_store

    def handle_transfer(self, block_hash, transfer):
        self.transfer_store.add(block_hash, transfer)
        self.account_store.transfer(transfer)
