import copy
import uuid

import attr

from gringotts.datastore import Amount, Order


class UnsupportedCurrencyError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class OrderDoesNotExistError(Exception):
    pass


@attr.s
class AccountSnapshot:
    uuid = attr.ib(type=str)
    orders = attr.ib(type=dict)
    balances = attr.ib(type=dict)

@attr.s
class Account:
    supported_currencies = {'BTC', 'USD'}

    uuid = attr.ib(factory=uuid.uuid4)
    open_orders = attr.ib(factory=dict)
    balances = attr.ib(factory=dict)

    def currency_valid(self, currency):
        if currency not in self.supported_currencies:
            raise UnsupportedCurrencyError(str(currency))

    def get_balance(self, currency):
        self.currency_valid(currency=currency)

        if self.balances.get(currency):
            return copy.deepcopy(self.balances[currency])
        else:
            return Amount.zero

    def credit(self, currency, amount):
        balance = self.get_balance(currency=currency)
        self.balances[currency] = balance.add(amount=amount)
        return self.get_balance(currency=currency)

    def debit(self, currency, amount):
        balance = self.get_balance(currency=currency)
        self.balances[currency] = balance.subtract(amount=amount)
        return self.get_balance(currency=currency)

    def get_open_orders(self):
        return self.open_orders

    def create_order(self, offered_currency, offered_amount, received_currency, received_amount):
        if self.get_balance(currency=offered_currency) > offered_amount:
            raise InsufficientFundsError(f'offered_currency: {str(offered_currency)} compared to {str(offered_amount)}')

        self.debit(currency=offered_currency,
                   amount=offered_amount)
        order = Order(offered_currency=offered_currency,
                      offered_amount=offered_amount,
                      received_currency=received_currency,
                      received_amount=received_amount)

        self.open_orders[order.uuid] = order

        return order

    def fill_order(self, order):
        if not self.open_orders.get(order):
            raise OrderDoesNotExistError(order.uuid)

        self.credit(currency=order.received_currency,
                    amount=order.received_amount)
        self.open_orders.pop(order.uuid, None)

    def split_prder(self, order, amount):
        if not self.open_orders.get(order.uuid):
            raise OrderDoesNotExistError(order.uuid)

        filled, remaining = order.split(amount=amount)
        self.fill_order(order=filled)
        self.open_orders[remaining.uuid] = remaining

        return filled, remaining

    def cancel_order(self, order):
        if not self.open_orders.get(order):
            raise OrderDoesNotExistError(order.uuid)

        self.credit(currency=order.offered_currency, amount=order.offered_amount)
        self.open_orders.pop(order.uuid, None)

    def create_snapshot(self):
        orders_snap = dict()
        for name, order in self.open_orders:
            orders_snap[name] = order.create_snapshot()

        balances_snap = dict()
        for name, balance in self.balances:
            balances_snap[name] = str(balance)

        snap = AccountSnapshot(uuid=str(self.uuid),
                               orders=orders_snap,
                               balances=balances_snap)

        return attr.asdict(snap)

    @staticmethod
    def load_snapshot(data):
        account = Account(data['uuid'])
        for name, order_snap in data['orders']:
            account.open_orders[name] = Order.load_snapshot(order_snap)
        for name, balance_snap in data['balances']:
            account.balances[name] = Amount(int(balance_snap))

        return account
