from copy import deepcopy
from typing import Union, Any, Tuple

from engine.node import Node


class Number:
    """Represents a number, variable, or external."""
    def __init__(self, n: Union[int, float, str]):
        self.initial = n
        self.queue = []

    # Operations

    def unary(self, op: str) -> 'Number':
        """Apply a unary operation to a number."""
        if op == 'ln':
            return self._ln()
        elif op == 'csc':
            return Number(1).binary('div', self.unary('sin'))
        elif op == 'sec':
            return Number(1).binary('div', self.unary('cos'))
        elif op == 'cot':
            return Number(1).binary('div', self.unary('tan'))
        elif op == 'arccsc':
            return Number(1).binary('div', self.unary('arcsin'))
        elif op == 'arcsec':
            return Number(1).binary('div', self.unary('arccos'))
        elif op == 'arccot':
            return Number(1).binary('div', self.unary('arctan'))
        else:
            clone = deepcopy(self)
            clone.queue.append((op,))
            return clone

    def binary(self, op: str, other: 'Number') -> 'Number':
        """Apply a binary operation to a number."""
        clone = deepcopy(self)
        clone.queue.append((op, other))
        return clone

    def _ln(self) -> 'Number':
        """Estimate the natural logarithm of a number."""
        n = Number(0)
        for k in range(0, 4):
            # 2k + 1
            common = Number(k).binary('mul', Number(2)).binary('add', Number(1))
            # 1 / (2k + 1)
            ln = Number(1).binary('div', common)
            # ((z - 1) / (z + 1))^(2k + 1)
            numer = self.binary('sub', Number(1))
            denom = self.binary('add', Number(1))
            rn = numer.binary('div', denom).binary('exp', common)
            # add product of terms
            n = n.binary('add', ln.binary('mul', rn))
        n = n.binary('mul', Number(2))
        return n

    # Resolutions

    def evaluate(self) -> Node:
        """Generate a YOLOL expression."""
        if type(self.initial) == str:
            node = Node(kind='variable', value=self.initial)
        else:
            node = Node(kind='number', value=self.initial)
        for op, *args in self.queue:
            if len(args) == 0:
                node = Node(kind=op, children=[node])
            elif len(args) == 1:
                node = Node(kind=op, children=[node, args[0].evaluate()])
            else:
                raise AssertionError('unrecognized item in queue: {}, {}'.format(op, args))
        return node

    def assign(self, index: int) -> Tuple[Node, 'Number']:
        """Generate a YOLOL assignment statement."""
        ident = 'n{}'.format(index)
        var = Node(kind='variable', value=ident)
        expr = self.evaluate()
        asn = Node(kind='assignment', children=[var, expr])
        return asn, Number(ident)
