import os

from flask import Flask
from api.rest.controller.block import init as init_block_controller
from api.rest.controller.account import init as init_account_controller
from handler.account import AccountHandler
from handler.block import BlockHandler, BlockRepeatedException
from storage.factory import StorageFactory
from storage.memory import MemoryStorage
from mock.blocks import mock

storage_factory = StorageFactory(MemoryStorage)
account_handler = AccountHandler(storage_factory)
block_handler = BlockHandler(storage_factory, account_handler)

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/api'

init_block_controller(app, block_handler)
init_account_controller(app, account_handler)

# if mock is false no test data is loaded
if "MOCK" not in os.environ or os.environ["MOCK"] != "false":
    blocks = mock()
    for block in blocks:
        block_handler.add_block(block)

