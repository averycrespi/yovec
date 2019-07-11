from operator import add, sub, mul, truediv, mod, pow, lt, le, gt, ge, eq, ne
from typing import Union


BINARY = {
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
        return Decimal(round(BINARY[op](self.value, other.value), 4))
