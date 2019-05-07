import copy
from typing import Optional, List, Any, Dict

import attr

from gringotts.datastore import OrderBook, Order


@attr.s
class Market:
    left_currency = attr.ib(type=Any)
    right_currency = attr.ib(type=Any)
    left_book = attr.ib(factory=OrderBook)
    right_book = attr.ib(factory=OrderBook)
    last_order = attr.ib(type=Optional[Order], default=None)

    def add_order(self, order: Order) -> List[Any]:
        if order.offered_currency == self.left_currency:
            book, other_book = self.right_book, self.left_book
        else:
            book, other_book = self.left_book, self.right_book

        flipped_order = copy.deepcopy(order)
        flipped_order.price = order.price.inverse()  # TODO: check if arr or string

        results = other_book.fill_orders_with(flipped_order)
        outcome = results.pop()

        if outcome.kind is ('order_filled' or 'order_partially_filled'):
            if outcome.order:
                self.last_order = outcome.order
            else:
                self.last_order = outcome.filled_order

        if outcome.kind != 'order_filled':
            outcome.residual_order.uuid = order.uuid
            results.append(book.add_order(outcome.residual_order))

        results.append(outcome)

        return results

    def get_last_price(self, currency: Any) -> Optional[int]:
        if not self.last_order:
            return None

        if self.last_order.offered_currency == currency:
            return self.last_order.price

        return self.last_order.price.inverse()

    def cancel_order(self, order: Order):
        if order.offered_currency == self.left_currency:
            book = self.right_book
        else:
            book = self.left_book

        book.cancel_order(order)

    def create_snapshot(self) -> Dict:
        return {
            'left':
                {
                    'currency': self.left_currency,
                    'book': self.left_book.create_snapshot(),
                },
            'right':
                {
                    'currency': self.right_currency,
                    'book': self.right_book.create_snapshot(),
                },
        }

    @staticmethod
    def load_snapshot(data: Dict):
        market = Market(data['left_currency'], data['right_currency'])
        market.left_book = OrderBook.load_snapshot(data=data['left']['book'])
        market.right_book = OrderBook.load_snapshot(data=data['right']['book'])

        return market
