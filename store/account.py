from store.generic import GenericStore
from storage.factory import StorageType
from model.account import *

class AccountStore(GenericStore):
    def init(self):
        self.account = self.storage_factory.branch('account', StorageType.KEY_VALUE)
        self.account_median = self.storage_factory.branch('account_median', StorageType.KEY_VALUE)
        self.account_transfers = self.storage_factory.branch('account_transfers', StorageType.KEY_VALUE)

    def set_balance(self, address, amount):
        balance = self.get_balance(address)
        if balance != None:
            raise AccountSetBalanceException()

        account_hash = get_account_hash(address)
        self.account.update(account_hash, amount)

    def transfer(self, transfer):
        # grab data and do some checks
        amount = get_amount(transfer)

        sender = get_sender(transfer)
        sender_balance = self.get_balance(sender)
        sender_hash = get_account_hash(sender)

        if sender_balance < amount:
            raise AccountTransferNotEnoughFunds()

        receiver = get_receiver(transfer)
        receiver_balance = self.get_balance(receiver)
        receiver_hash = get_account_hash(receiver)

        # update balance
        self.account.update(sender_hash, sender_balance - amount)
        self.account.update(receiver_hash, receiver_balance + amount)

        # update transfer list
        sender_statement = self.get_statement(sender)
        receiver_statement = self.get_statement(receiver)

        self.account_transfers.update(sender_hash, sender_statement + [transfer])
        self.account_transfers.update(receiver_hash, receiver_statement + [transfer])

    def revert(self, transfer):
        # create a revert event of the given transfer
        reverted_transfer = transfer.copy()
        reverted_transfer = set_sender(reverted_transfer, get_receiver(transfer))
        reverted_transfer = set_receiver(reverted_transfer, get_sender(transfer))
        reverted_transfer = set_revert_type(reverted_transfer)

        self.transfer(reverted_transfer)

    def get_balances(self):
        return self.account.get_all()

    def get_balance(self, address):
        return self.account.get(get_account_hash(address))

    def get_statement(self, address):
        return self.account_transfers.get(get_account_hash(address)) or []

class AccountSetBalanceException(Exception):
    pass

class AccountTransferNotEnoughFunds(Exception):
    pass
