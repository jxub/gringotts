import attr
import copy


@attr.s
class BookStore:
    pass



@attr.s
class OrderBook:
    store = attr.ib(factory=BookStore)

    def fill_orders_with(self, order):
        orig_order = order
        order = copy.deepcopy(order)

        closed = []
        amount_filled = Ratio()