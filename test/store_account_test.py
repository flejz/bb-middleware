import unittest

from storage.memory import MemoryStorage
from store.account import AccountStore, AccountSetBalanceException, AccountTransferNotEnoughFunds
from model.account import get_account_hash

class TestAccountStore(unittest.TestCase):
    def setUp(self):
        self.account_store = AccountStore(MemoryStorage(), "account")

    def test_should_set_balance_when_non_existent(self):
        self.account_store.set_balance("xyz", 10)

    def test_should_raise_exception_on_set_balance_when_existent(self):
        self.account_store.set_balance("xyz", 10)
        with self.assertRaises(AccountSetBalanceException):
            self.account_store.set_balance("xyz", 10)

    def test_should_get_balance_when_existent(self):
        self.account_store.set_balance("xyz", 10)
        self.assertEqual(self.account_store.get_balance("xyz"), 10)

    def test_should_not_get_balance_when_non_existent(self):
        self.assertEqual(self.account_store.get_balance("xyz"), None)

    def test_should_properly_transfer_when_enough_funds_available(self):
        transfer = { "sender": "abc", "receiver": "xyz", "amount": 10 }
        self.account_store.set_balance("abc", 10)
        self.account_store.set_balance("xyz", 0)
        self.account_store.transfer(transfer)
        self.assertEqual(self.account_store.get_balance("abc"), 0)
        self.assertEqual(self.account_store.get_balance("xyz"), 10)

    def test_should_raise_exception_on_transfer_when_not_enough_funds(self):
        transfer = { "sender": "abc", "receiver": "xyz", "amount": 10 }
        self.account_store.set_balance("abc", 5)
        self.account_store.set_balance("xyz", 0)
        with self.assertRaises(AccountTransferNotEnoughFunds):
            self.account_store.transfer(transfer)

    def test_should_get_all_balances(self):
        transfer = { "sender": "abc", "receiver": "xyz", "amount": 3 }
        self.account_store.set_balance("abc", 10)
        self.account_store.set_balance("xyz", 0)
        self.account_store.transfer(transfer)

        balances = self.account_store.get_balances()
        print(balances)
        self.assertEqual(len(balances.items()), 2)
        self.assertEqual(balances[get_account_hash("abc")], 7)
        self.assertEqual(balances[get_account_hash("xyz")], 3)


if __name__ == "__main__":
    unittest.main()
