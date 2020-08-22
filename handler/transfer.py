class TransferHandler():
    def __init__(self, account_store, transfer_store):
        self.account_store = account_store
        self.transfer_store = transfer_store

    def handle_transfer(self, block, transfer):
        self.transfer_store.add(block, transfer)
        self.account_store.transfer(transfer)

        return self.transfer_store.get_transfers_by_block(block)
