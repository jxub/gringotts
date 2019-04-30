import typing as t
from enum import Enum

import attr

from gringotts.datastore import DataStore




class InvalidOperation(Exception):
    pass

@attr.s
class Engine:
    datastore = attr.ib(factory=DataStore)
    op_handlers = attr.ib(factory=dict, type=t.Dict[t.Callable])

    def __attrs_post_init__(self):
        self.op_handlers[Operation.ADD_DEPOSIT] = lambda op: self.datastore.deposit(op)
        self.op_handlers[Operation.WITHDRAW_FUNDS] = lambda op: self.datastore.withdraw(op)
        self.op_handlers[Operation.CREATE_LIMIT_ORDER] = lambda op: self.datastore.place_order(op)

    def execute_operation(self, op):
        try:
            if self.op_handlers.get(op.kind):
                return self.op_handlers[op.kind](op)
        except AttributeError:
            raise InvalidOperation(str(op))
