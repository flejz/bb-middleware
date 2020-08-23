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

    def last_block(self):
        current_height = -1
        current_block = None
        for block_hash in self.chain.get_all():
            block = self.get_block(block_hash)
            if get_block_height(block) >= current_height:
                current_height = get_block_height(block)
                current_block = block

        return current_block

    def last_block_hash(self):
        return get_block_hash(self.last_block())

    def get_height(self):
        return get_block_height(self.last_block())

    def get_block(self, block_hash):
        return self.block.get(block_hash)

    def add_block(self, block):

        # applies the revert strategy
        block_hash = get_block_hash(block)
        block_prevhash = get_block_prevhash(block)
        block_height = get_block_height(block)
        if self.get_block(block_hash) != None:
            raise BlockRepeatedException()

        # grabbind data from the last block
        last_block = self.last_block()
        last_block_hash = get_block_hash(last_block)
        last_block_height = get_block_height(last_block)

        # adding new block
        self.block.update(block_hash, block)

        blocks_to_revert = []
        blocks_to_apply = []

        if block_height == 0: # genesis block
            blocks_to_apply.append(block_hash)
        elif block_height > last_block_height:
            if last_block_hash == block_prevhash:
                blocks_to_apply.append(block_hash)
            else:

                blocks_to_revert = self.diff_block_chain(last_block, block)
                blocks_to_apply = self.get_block_chain(block)

        elif block_height == last_block_height:
            blocks_to_revert = self.diff_block_chain(last_block, block)
            blocks_to_apply = self.get_block_chain(block)

        self.revert_block_chain(blocks_to_revert)
        self.apply_block_chain(blocks_to_apply)

        # updating data
        self.chain.add(block_hash)

    def diff_block_chain(self, block_base, block_compare):
        block_chain_base = self.get_block_chain(block_base)
        block_chain_compare = self.get_block_chain(block_compare)
        block_chain_compare = set(block_chain_compare)

        return [block_hash for block_hash in block_chain_base if block_hash not in block_chain_compare]

    def get_block_chain(self, block = None, block_chain = []):
        if block == None:
            block = self.last_block()

        if get_block_height(block) <= 0:
            return block_chain

        block_hash = get_block_hash(block)
        block_prevhash = get_block_prevhash(block)
        return self.get_block_chain(self.get_block(block_prevhash), block_chain + [block_hash])


    def apply_block(self, block):
        if has_block_balances(block):
            for address, amount in get_block_balances(block).items():
                self.account_handler.set_balance(address, amount)

        if has_block_balances(block):
            for transfer in get_block_transfers(block):
                self.account_handler.transfer(transfer)

        # self.chain_reverted.remove(get_block_hash(block))

    def apply_block_chain(self, block_chain):
        for block_hash in block_chain:
            block = self.get_block(block_hash)
            self.apply_block(block)

    def revert_block(self, block):
        if has_block_transfers(block):
            for transfer in get_block_transfers(block):
                self.account_handler.revert(transfer)

        self.chain_reverted.add(get_block_hash(block))

    def revert_block_chain(self, block_chain):
        for block_hash in block_chain:
            block = self.get_block(block_hash)
            self.revert_block(block)

    def get_block_chain_bkp(self):
        return self.chain.get_all() or []

    def get_block_chain_reverted(self):
        return self.chain_reverted.get_all() or []

class BlockRepeatedException(Exception):
    pass
