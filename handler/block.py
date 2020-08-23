from handler.generic import GenericHandler
from storage.factory import StorageType
from model.block import *

class BlockHandler(GenericHandler):
    def __init__(self, storage_factory, account_handler):
        GenericHandler.__init__(self, storage_factory)
        self.account_handler = account_handler

    def init(self):
        self.block = self.storage_factory.branch('block', StorageType.KEY_VALUE)
        self.chain = self.storage_factory.branch('chain', StorageType.LIST)
        self.chain_reverted = self.storage_factory.branch('chain_reverted', StorageType.LIST)

    def last_hash(self):
        return self.chain.last()

    def get_height(self):
        block_hash = self.last_hash()
        return -1 if block_hash is None else get_block_height(self.get_block(block_hash))

    def get_block(self, block_hash):
        return self.block.get(block_hash)

    def add_block(self, block):
        block_hash = get_block_hash(block)
        if self.get_block(block_hash) != None:
            raise BlockRepeatedException()

        # processing balances
        self.set_balances(block)

        # revert on reorder
        self.revert_up_to(block, self.chain.last())

        # processing blocks
        self.add_transfers(block)

        # updating data
        self.block.update(block_hash, block)
        self.chain.add(block_hash)

    def add_transfers(self, block):
        for transfer in get_block_transfers(block):
            self.account_handler.transfer(transfer)

    def set_balances(self, block):
        if not has_block_balances(block):
            return

        for address, amount in get_block_balances(block).items():
            self.account_handler.set_balance(address, amount)

    def revert_up_to(self, block, prev_block_hash):
        if prev_block_hash == None:
            return

        prev_block = self.get_block(prev_block_hash)
        if get_block_height(prev_block) >= get_block_height(block):
            self.revert_transfers(prev_block)
            self.chain_reverted.add(prev_block_hash)
            self.revert_up_to(block, get_block_prevhash(prev_block))

    def revert_transfers(self, block):
        for transfer in get_block_transfers(block):
            self.account_handler.revert(transfer)

    def get_chain(self):
        return self.chain.get_all() or []

    def get_chain_reverted(self):
        return self.chain_reverted.get_all() or []

class BlockRepeatedException(Exception):
    pass
