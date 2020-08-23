import unittest
import statistics

from storage.factory import StorageFactory
from storage.memory import MemoryStorage
from store.account import AccountStore, AccountSetBalanceException, AccountNotEnoughFundsException
from model.account import get_account_hash

class TestAccountStore(unittest.TestCase):
    def setUp(self):
        self.account_store = AccountStore(StorageFactory(MemoryStorage))

    def test_should_set_balance_when_non_existent(self):
        self.account_store.set_balance("bar", 10)

    def test_should_raise_exception_on_set_balance_when_existent(self):
        self.account_store.set_balance("bar", 10)
        with self.assertRaises(AccountSetBalanceException):
            self.account_store.set_balance("bar", 10)

    def test_should_get_balance_when_existent(self):
        self.account_store.set_balance("bar", 10)
        self.assertEqual(self.account_store.get_balance("bar"), 10)

    def test_should_not_get_balance_when_non_existent(self):
        self.assertEqual(self.account_store.get_balance("bar"), None)

    def test_should_properly_transfer_when_enough_funds_available(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 10 }
        self.account_store.set_balance("foo", 10)
        self.account_store.set_balance("bar", 0)
        self.account_store.transfer(transfer)
        self.assertEqual(self.account_store.get_balance("foo"), 0)
        self.assertEqual(self.account_store.get_balance("bar"), 10)

    def test_should_raise_exception_on_transfer_when_not_enough_funds(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 10 }
        self.account_store.set_balance("foo", 5)
        self.account_store.set_balance("bar", 0)
        with self.assertRaises(AccountNotEnoughFundsException):
            self.account_store.transfer(transfer)

    def test_should_get_balances(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 3 }
        self.account_store.set_balance("foo", 10)
        self.account_store.set_balance("bar", 0)
        self.account_store.transfer(transfer)

        balances = self.account_store.get_balances()
        self.assertEqual(len(balances.items()), 2)
        self.assertEqual(balances[get_account_hash("foo")], 7)
        self.assertEqual(balances[get_account_hash("bar")], 3)

    def test_should_get_balance(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 3 }
        self.account_store.set_balance("foo", 10)
        self.account_store.set_balance("bar", 0)
        self.account_store.transfer(transfer)

        self.assertEqual(self.account_store.get_balance("foo"), 7)
        self.assertEqual(self.account_store.get_balance("bar"), 3)

    def test_should_get_statement(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 3 }
        self.account_store.set_balance("foo", 10)
        self.account_store.set_balance("bar", 0)
        self.account_store.transfer(transfer)
        self.account_store.transfer(transfer)

        self.assertEqual(self.account_store.get_balance("foo"), 4)
        self.assertEqual(self.account_store.get_balance("bar"), 6)
        self.assertEqual(self.account_store.get_statement("foo"), [transfer, transfer])
        self.assertEqual(self.account_store.get_statement("bar"), [transfer, transfer])

    def test_should_revert_a_transfer(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 3 }
        self.account_store.set_balance("foo", 10)
        self.account_store.set_balance("bar", 0)

        self.account_store.transfer(transfer)
        self.assertEqual(self.account_store.get_balance("foo"), 7)
        self.assertEqual(self.account_store.get_balance("bar"), 3)

        self.account_store.revert(transfer)
        self.assertEqual(self.account_store.get_balance("foo"), 10)
        self.assertEqual(self.account_store.get_balance("bar"), 0)

    def test_should_calculate_median(self):
        transfers = [
                { "sender": "foo", "receiver": "bar", "amount": 1 },
                { "sender": "foo", "receiver": "baz", "amount": 2 },
                { "sender": "bar", "receiver": "foo", "amount": 3 },
                { "sender": "bar", "receiver": "baz", "amount": 4 },
                { "sender": "baz", "receiver": "foo", "amount": 5 },
                { "sender": "baz", "receiver": "bar", "amount": 6 },
        ]
        foo = [-1, -2, 3, 5]
        bar = [1, -3, -4, 6]
        baz = [2, 4, -5, -6]

        self.account_store.set_balance("foo", 100)
        self.account_store.set_balance("bar", 100)
        self.account_store.set_balance("baz", 100)
        for transfer in transfers:
            self.account_store.transfer(transfer)

        self.assertEqual(self.account_store.get_median("foo"), statistics.median(foo))
        self.assertEqual(self.account_store.get_median("bar"), statistics.median(bar))
        self.assertEqual(self.account_store.get_median("baz"), statistics.median(baz))


if __name__ == "__main__":
    unittest.main()
