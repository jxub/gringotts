from __future__ import annotations

import uuid
import attr

from typing import Optional, Tuple

from gringotts.datastore import Amount, Ratio, Account


@attr.s
class Order:
    account = attr.ib(type=Account)
    offered_currency = attr.ib(type=str)
    offered_amount = attr.ib(type=Amount)
    received_currency = attr.ib(type=str)
    received_amount = attr.ib(type=Amount)

    uuid = attr.ib(factory=uuid.uuid4, type=Optional[str])

    price = attr.ib(init=False, type=Ratio)

    def __attrs_post_init__(self):
        self.price = Ratio(
            numerator=self.offered_amount,
            denominator=self.received_amount
        )

    def clone(self, reversed: bool = False):
        if reversed:
            return Order(
                account=self.account,
                offered_currency=self.received_currency,
                offered_amount=self.received_amount,
                received_currency=self.offered_currency,
                received_amount=self.offered_amount,
                uuid=None
            )

        return Order(
            account=self.account,
            offered_currency=self.offered_currency,
            offered_amount=self.offered_amount,
            received_currency=self.received_currency,
            received_amount=self.received_amount,
            uuid=self.uuid,
        )

    def split(self, amount) -> Tuple[Order, Order]:
        received_amount = self.received_amount / self.offered_amount * amount

        filled = Order(
            account=self.account,
            offered_currency=self.offered_currency,
            offered_amount=amount,
            received_currency=self.received_currency,
            received_amount=received_amount,
            uuid=self.uuid
        )

        remaining = Order(
            account=self.account,
            offered_currency=self.offered_currency,
            offered_amount=self.offered_amount - amount,
            received_currency=self.received_currency,
            received_amount=self.received_amount - received_amount
        )

        return filled, remaining

    def create_snapshot(self):
        return {
            'account_id': self.account.uuid if self.account.uuid else self.account,
            'offered_currency': self.offered_currency,
            'offered_amount': str(self.offered_amount),
            'received_currency': self.received_currency,
            'received_amount': str(self.received_amount),
            'uuid': self.uuid,
        }

    @staticmethod
    def load_snapshot(snap):
        return Order(
            account=snap['account_id'],
            offered_currency=snap['offered_currency'],
            offered_amount=Amount.load_snapshot(snap['offered_amount']),
            received_currency=snap['received_currency'],
            received_amount=Amount.load_snapshot(snap['received_amount']),
            uuid=snap['uuid'],
        )
