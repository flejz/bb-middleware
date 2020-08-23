def get_block_hash(block):
    return None if block is None else block["hash"]

def get_block_prevhash(block):
    return None if block is None else block["prevhash"]

def get_block_height(block):
    return -1 if block is None else block["number"]

def get_block_balances(block):
    return {} if not has_block_balances(block) else block["balances"]

def has_block_balances(block):
    return False if block is None else "balances" in block

def get_block_transfers(block):
    return [] if block is None else block["transfers"]

def has_block_transfers(block):
    return False if block is None else "transfers" in block
