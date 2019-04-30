from enum import Enum

from bunch import Bunch


class Operation(Enum):
    ADD_DEPOSIT = 1
    WITHDRAW_FUNDS = 2
    CREATE_LIMIT_ORDER = 3
    CANCEL_ORDER = 4
    GET_BALANCES = 5
    OPEN_ORDERS = 6
    ORDER_INFO = 7
    BALANCES = 8
    TICKER = 9
    SEND_BITCOINS = 10


create_results = Bunch(
    ADD_DEPOSIT=lambda _: None,
    BALANCES=lambda account_id, balances: Bunch(
        result=Operation.OPEN_ORDERS,
        account=account_id,
        balances=balances
    ),
    OPEN_ORDERS=lambda account_id, orders: Bunch(
        result=Operation.OPEN_ORDERS,
        account=account_id,
        orders=orders
    ),
    TICKER=lambda currency, bid, ask, last: Bunch(
        result=Operation.TICKER,
        currency=currency,
        bid=bid,
        ask=ask,
        last=last
    ),
)
