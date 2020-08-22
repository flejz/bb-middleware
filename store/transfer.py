from store.generic import GenericStore
from model.block import get_block_hash
from model.account import get_account_hash

class TransferStore(GenericStore):
    def add(self, block, transfer):
        self.add_block(self, block, transfer)
        self.add_account(self, transfer["sender"], transfer)
        self.add_account(self, transfer["receiver"], transfer)

    def add_block(self, block, transfer):
        block_hash = get_block_hash(block)
        transfers = self.get_transfers_by_block(block)
        return self.update(block_hash, transfers + [transfer])

    def add_account(self, address, transfer):
        account_hash = get_account_hash(address)
        transfers = self.get_transfers_by_account(address)
        return self.update(account_hash, transfers + [transfer])

    def get_transfers_by_block(self, block):
        block_hash = get_block_hash(block)
        return self.get(block_hash) or []

    def get_transfers_by_account(self, address):
        account_hash = get_account_hash(address)
        return self.get(account_hash) or []
