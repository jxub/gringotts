import attr
import copy

from gringotts.datastore import Ratio
from typing import List, Optional


@attr.s
class BookStore:
    pass



@attr.s
class OrderBook:
    store = attr.ib(factory=BookStore)

    def fill_orders_with(self, order) -> List:
        orig_order = order
        order = copy.deepcopy(order)

        closed = []
        amount_filled = Ratio()
        # TODO

    @staticmethod
    def load_snapshot(data):
        return str(data)  # todo
