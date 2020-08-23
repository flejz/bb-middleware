import json

from handler.account import AccountHandler
from handler.block import BlockHandler
from storage.factory import StorageFactory
from storage.memory import MemoryStorage

storage_factory = StorageFactory(MemoryStorage)
account_handler = AccountHandler(storage_factory)
block_handler = BlockHandler(storage_factory, account_handler)

def run(file_path, show_median):
    blockchain_file = open(file_path, "r")
    blocks = json.load(blockchain_file)
    for block in blocks:
        block_handler.add_block(block)

    if show_median:
        return account_handler.get_medians()

    return account_handler.get_balances()
