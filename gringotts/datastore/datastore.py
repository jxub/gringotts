import attr

from gringotts.datastore import BalanceSheet


@attr.s
class DataStore:
    balance_sheet = attr.ib(type=BalanceSheet)
