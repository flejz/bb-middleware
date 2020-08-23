def get_address(account):
    return None if account is None  else account["address"]

def get_amount(transfer):
    return transfer["amount"]

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

def get_revert(transfer):
    return False if not "revert" in transfer else transfer["revert"]

def set_revert(base_transfer):
    transfer = base_transfer.copy()
    transfer["revert"] = True
    return transfer
