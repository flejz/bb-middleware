from store.generic import GenericStore
from model.account import get_account_hash
from model.transfer import get_sender, get_receiver, get_amount

class AccountStore(GenericStore):
    def set_balance(self, address, amount):
        balance = self.get_balance(address)
        if balance != None:
            raise AccountSetBalanceException()

        account_hash = get_account_hash(address)
        self.update(account_hash, amount)

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

        self.update(sender_hash, sender_balance - amount)
        self.update(receiver_hash, receiver_balance + amount)

    def get_balance(self, address):
        return self.get(get_account_hash(address))

    def get_balances(self):
        return self.get_all()

class AccountSetBalanceException(Exception):
    pass

class AccountTransferNotEnoughFunds(Exception):
    pass
