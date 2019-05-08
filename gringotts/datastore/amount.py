import attr
import copy


@attr.s(init=False)
class Amount(int):

    def __init__(self, num: int):
        super().__init__(num)

    def clone(self):
        return copy.deepcopy(self)

    def create_snapshot(self):
        return str(self)

    @staticmethod
    def load_snapshot(data):
        return Amount(int(data))

    @staticmethod
    def zero():
        return Amount(0)

    @staticmethod
    def one():
        return Amount(1)
