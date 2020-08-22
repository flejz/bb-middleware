def get_block_hash(block):
    return "b_%s" % block["hash"]

def get_block_height(block):
    return None if block is None else block["number"]
