import unittest
import statistics

from storage.factory import StorageFactory
from storage.memory import MemoryStorage
from handler.account import AccountHandler, AccountSetBalanceException

class TestAccountHandler(unittest.TestCase):
    def setUp(self):
        self.account_handler = AccountHandler(StorageFactory(MemoryStorage))

    def test_should_set_balance_when_non_existent(self):
        self.account_handler.set_balance("bar", 10)

    def test_should_raise_exception_on_set_balance_when_existent(self):
        self.account_handler.set_balance("bar", 10)
        with self.assertRaises(AccountSetBalanceException):
            self.account_handler.set_balance("bar", 10)

    def test_should_get_balance_when_existent(self):
        self.account_handler.set_balance("bar", 10)
        self.assertEqual(self.account_handler.get_balance("bar"), 10)

    def test_should_not_get_balance_when_non_existent(self):
        self.assertEqual(self.account_handler.get_balance("bar"), None)

    def test_should_properly_transfer_when_enough_funds_available(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 10 }
        self.account_handler.set_balance("foo", 10)
        self.account_handler.set_balance("bar", 0)
        self.account_handler.transfer(transfer)
        self.assertEqual(self.account_handler.get_balance("foo"), 0)
        self.assertEqual(self.account_handler.get_balance("bar"), 10)

    def test_should_not_transfer_when_not_enough_funds(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 10 }
        self.account_handler.set_balance("foo", 5)
        self.account_handler.set_balance("bar", 0)
        self.account_handler.transfer(transfer)
        self.assertEqual(self.account_handler.get_balance("foo"), 5)
        self.assertEqual(self.account_handler.get_balance("bar"), 0)

    def test_should_get_balances(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 3 }
        self.account_handler.set_balance("foo", 10)
        self.account_handler.set_balance("bar", 0)
        self.account_handler.transfer(transfer)

        balances = self.account_handler.get_balances()
        self.assertEqual(len(balances.items()), 2)
        self.assertEqual(balances["foo"], 7)
        self.assertEqual(balances["bar"], 3)

    def test_should_get_balance(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 3 }
        self.account_handler.set_balance("foo", 10)
        self.account_handler.set_balance("bar", 0)
        self.account_handler.transfer(transfer)

        self.assertEqual(self.account_handler.get_balance("foo"), 7)
        self.assertEqual(self.account_handler.get_balance("bar"), 3)

    def test_should_get_statement(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 3 }
        self.account_handler.set_balance("foo", 10)
        self.account_handler.set_balance("bar", 0)
        self.account_handler.transfer(transfer)
        self.account_handler.transfer(transfer)

        self.assertEqual(self.account_handler.get_balance("foo"), 4)
        self.assertEqual(self.account_handler.get_balance("bar"), 6)
        self.assertEqual(self.account_handler.get_statement("foo"), [transfer, transfer])
        self.assertEqual(self.account_handler.get_statement("bar"), [transfer, transfer])

    def test_should_revert_a_transfer(self):
        transfer = { "sender": "foo", "receiver": "bar", "amount": 3 }
        self.account_handler.set_balance("foo", 10)
        self.account_handler.set_balance("bar", 0)

        self.account_handler.transfer(transfer)
        self.assertEqual(self.account_handler.get_balance("foo"), 7)
        self.assertEqual(self.account_handler.get_balance("bar"), 3)

        self.account_handler.revert(transfer)
        self.assertEqual(self.account_handler.get_balance("foo"), 10)
        self.assertEqual(self.account_handler.get_balance("bar"), 0)

    def test_should_revert_a_transfer_even_without_enough_funds(self):
        # the reason this is allowed is that it's only gonna happen given
        # a chain ov events incoming from new blocks.
        # after a successfull block revert chain, and the new transfer coming
        # in the amount value will be correct
        transfer = { "sender": "foo", "receiver": "bar", "amount": 3 }
        self.account_handler.set_balance("foo", 0)
        self.account_handler.set_balance("bar", 0)

        self.account_handler.revert(transfer)
        self.assertEqual(self.account_handler.get_balance("foo"), 3)
        self.assertEqual(self.account_handler.get_balance("bar"), -3)

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

        self.account_handler.set_balance("foo", 100)
        self.account_handler.set_balance("bar", 100)
        self.account_handler.set_balance("baz", 100)
        for transfer in transfers:
            self.account_handler.transfer(transfer)

        self.assertEqual(self.account_handler.get_median("foo"), statistics.median(foo))
        self.assertEqual(self.account_handler.get_median("bar"), statistics.median(bar))
        self.assertEqual(self.account_handler.get_median("baz"), statistics.median(baz))


if __name__ == "__main__":
    unittest.main()
