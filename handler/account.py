import statistics

from handler.generic import GenericHandler
from storage.factory import StorageType
from model.account import *

class AccountHandler(GenericHandler):
    def init(self):
        self.account = self.storage_factory.branch('account', StorageType.KEY_VALUE)
        self.account_median = self.storage_factory.branch('account_median', StorageType.KEY_VALUE)
        self.account_transfers = self.storage_factory.branch('account_transfers', StorageType.KEY_VALUE)
        self.account_transfers_failed = self.storage_factory.branch('account_transfers_failed', StorageType.KEY_VALUE)

    def get_balances(self):
        return self.account.get_all()

    def get_balance(self, address):
        return self.account.get(address)

    def set_balance(self, address, amount):
        balance = self.get_balance(address)
        if balance != None:
            raise AccountSetBalanceException()

        self.account.update(address, amount)

    def get_statement(self, address):
        return self.account_transfers.get(address) or []

    def get_failed(self, address):
        return self.account_transfers_failed.get(address) or []

    def get_medians(self):
        return self.account_median.get_all()

    def get_median(self, address):
        return self.account_median.get(address)

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
        is_revert = get_revert(transfer)

        sender = get_sender(transfer)
        sender_balance = self.get_balance(sender)

        receiver = get_receiver(transfer)
        receiver_balance = self.get_balance(receiver)

        if not is_revert and (sender_balance is None or sender_balance < amount):
            sender_transfers_failed = self.get_failed(sender)
            receiver_transfers_failed = self.get_failed(receiver)

            self.account_transfers_failed.update(sender, sender_transfers_failed + [transfer])
            self.account_transfers_failed.update(receiver, receiver_transfers_failed + [transfer])
            return

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
        reverted_transfer = set_revert(reverted_transfer)

        self.transfer(reverted_transfer)

class AccountSetBalanceException(Exception):
    pass
