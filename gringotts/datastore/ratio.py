import attr

from gringotts.datastore import Amount

@attr.s
class Ratio:
    numerator = attr.ib(type=Amount, default=Amount.zero())
    denominator = attr.ib(type=Amount, default=Amount.one())

    def __attrs_post_init__(self):
        if self.denominator == 0:
            raise ZeroDivisionError('denominator can\'t be 0')

        gcd = Amount

