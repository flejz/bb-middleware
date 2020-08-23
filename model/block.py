def get_block_hash(block):
    return block["hash"]

def get_block_prevhash(block):
    return block["prevhash"]

def get_block_height(block):
    return None if block is None else block["number"]

def get_block_balances(block):
    return {} if not has_block_balances(block) else block["balances"]

def has_block_balances(block):
    return "balances" in block

def get_block_transfers(block):
    return [] if block is None else block["transfers"]
