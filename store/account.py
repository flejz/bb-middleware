from store.generic import GenericStore
from storage.factory import StorageType
from model.account import get_account_hash
from model.transfer import get_sender, get_receiver, get_amount

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
        amount = get_amount(transfer)

        sender = get_sender(transfer)
        sender_balance = self.get_balance(sender)
        sender_hash = get_account_hash(sender)

        if sender_balance < amount:
            raise AccountTransferNotEnoughFunds()

        receiver = get_receiver(transfer)
        receiver_balance = self.get_balance(receiver)
        receiver_hash = get_account_hash(receiver)

        self.account.update(sender_hash, sender_balance - amount)
        self.account.update(receiver_hash, receiver_balance + amount)

        sender_statement = self.get_statement(sender)
        receiver_statement = self.get_statement(receiver)

        self.account_transfers.update(sender_hash, sender_statement + [transfer])
        self.account_transfers.update(receiver_hash, receiver_statement + [transfer])

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
