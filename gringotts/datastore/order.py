import uuid
import attr


@attr.s
class Order:
    offered_currency = attr.ib()
    offered_amount = attr.ib()
    received_currency = attr.ib()
    received_amount = attr.ib()

    uuid = attr.ib(factory=uuid.uuid4)

    def split(self, amount):

        filled = Order()

        remaining = Order()

        return filled, remaining

    def create_snapshot(self):
        return attr.asdict(self)

    @staticmethod
    def load_snapshot(self, snap):
        return Order(uuid=snap['uuid']) # TODO
