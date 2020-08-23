from handler.account import AccountHandler
from handler.block import BlockHandler
from storage.factory import StorageFactory
from storage.memory import MemoryStorage

storage_factory = StorageFactory(MemoryStorage)
account_handler = AccountHandler(storage_factory)
block_handler = BlockHandler(storage_factory, account_handler)

def event_handler(block):
    block_handler.add_block(block)

# some fake
ethereum_network = { "listen": lambda fn: fn }
ethereum_network.listen(event_handler)
