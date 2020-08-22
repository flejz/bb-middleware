def get_account_hash(address):
    return address

def get_sender(transfer):
    return transfer["sender"]

def set_sender(base_transfer, value):
    transfer = base_transfer.copy()
    transfer["sender"] = value
    return transfer

def get_receiver(transfer):
    return transfer["receiver"]

def set_receiver(base_transfer, value):
    transfer = base_transfer.copy()
    transfer["receiver"] = value
    return transfer

def get_amount(transfer):
    return transfer["amount"]

def set_revert_type(base_transfer):
    transfer = base_transfer.copy()
    transfer["type"] = "revert"
    return transfer
