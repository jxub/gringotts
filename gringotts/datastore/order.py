import uuid
import attr

from typing import Optional

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

    def split(self, amount):
        received_amount = self.received_amount / self.offered_amount * amount

        filled = Order(

        )

        remaining = Order()

        return filled, remaining

    def create_snapshot(self):
        return attr.asdict(self)

    @staticmethod
    def load_snapshot(snap):
        return Order(uuid=snap['uuid'])  # TODO
