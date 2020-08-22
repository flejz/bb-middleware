def get_block_hash(block):
    return block["hash"]

def get_block_prevhash(block):
    return block["prevhash"]

def get_block_height(block):
    return None if block is None else block["number"]
