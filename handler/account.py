import statistics

from handler.generic import GenericHandler
from storage.factory import StorageType
from model.account import *

class AccountHandler(GenericHandler):
    def init(self):
        self.account = self.storage_factory.branch('account', StorageType.KEY_VALUE)
        self.account_median = self.storage_factory.branch('account_median', StorageType.KEY_VALUE)
        self.account_transfers = self.storage_factory.branch('account_transfers', StorageType.KEY_VALUE)

    def get_balances(self):
        return self.account.get_all()

    def get_balance(self, address):
        return self.account.get(get_account_hash(address))

    def set_balance(self, address, amount):
        balance = self.get_balance(address)
        if balance != None:
            raise AccountSetBalanceException()

        account_hash = get_account_hash(address)
        self.account.update(account_hash, amount)

    def get_statement(self, address):
        return self.account_transfers.get(get_account_hash(address)) or []

    def get_median(self, address):
        return self.account_median.get(get_account_hash(address)) or None

    def update_median(self, address):
        amounts = []
        statement = self.get_statement(address)
        for transfer in statement:
            amount = get_amount(transfer)
            amount = amount * -1 if get_sender(transfer) == address else amount
            amounts.append(amount)

        self.account_median.update(address, statistics.median(amounts))

    def transfer(self, transfer):
        # grab data and do some checks
        amount = get_amount(transfer)

        sender = get_sender(transfer)
        sender_balance = self.get_balance(sender)

        if sender_balance < amount:
            raise AccountNotEnoughFundsException()

        receiver = get_receiver(transfer)
        receiver_balance = self.get_balance(receiver)

        # update balance
        self.account.update(sender, sender_balance - amount)
        self.account.update(receiver, receiver_balance + amount)

        # update transfer list
        sender_statement = self.get_statement(sender)
        receiver_statement = self.get_statement(receiver)

        self.account_transfers.update(sender, sender_statement + [transfer])
        self.account_transfers.update(receiver, receiver_statement + [transfer])

        self.update_median(sender)
        self.update_median(receiver)

    def revert(self, transfer):
        # create a revert event of the given transfer
        reverted_transfer = transfer.copy()
        reverted_transfer = set_sender(reverted_transfer, get_receiver(transfer))
        reverted_transfer = set_receiver(reverted_transfer, get_sender(transfer))
        reverted_transfer = set_revert_type(reverted_transfer)

        self.transfer(reverted_transfer)

class AccountSetBalanceException(Exception):
    pass

class AccountNotEnoughFundsException(Exception):
    pass
