from operator import add, sub, mul, truediv, mod, pow, lt, le, gt, ge, eq, ne, and_, or_
from typing import Union


ARITHMETIC = {
    'add': add,
    'sub': sub,
    'mul': mul,
    'div': truediv,
    'mod': mod,
    'exp': pow,
    'lt': lt,
    'le': le,
    'gt': gt,
    'ge': ge,
    'eq': eq,
    'ne': ne
}

BOOLEAN = {
    'and': and_,
    'or': or_
}


class Decimal:
    """Represents a limited-precision decimal."""
    def __init__(self, value: Union[float, str]):
        self.value = float(value)

    def __str__(self):
        if self.value.is_integer():
            return str(int(self.value))
        else:
            return str(self.value)

    def binary(self, op: str, other: 'Decimal') -> 'Decimal':
        """Apply a binary operation to two decimals."""
        try:
            return Decimal(round(ARITHMETIC[op](self.value, other.value), 4))
        except KeyError:
            left = int(0 == self.value)
            right = int(0 == other.value)
            return Decimal(round(BOOLEAN[op](left, right), 4))
