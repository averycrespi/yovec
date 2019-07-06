from copy import deepcopy
from typing import Union, Any, Tuple

from engine.node import Node


class SimpleNumber:
    """Represents a number, variable, or external."""
    def __init__(self, n: Union[int, float, str]):
        self.initial = n
        self.queue = []

    # Operations

    def unary(self, op: str) -> 'SimpleNumber':
        """Apply a unary operation to a simple number."""
        if op == 'ln':
            return self._ln()
        else:
            clone = deepcopy(self)
            clone.queue.append((op,))
            return clone

    def binary(self, op: str, sn: 'SimpleNumber') -> 'SimpleNumber':
        """Apply a binary operation to a simple number."""
        clone = deepcopy(self)
        clone.queue.append((op, sn))
        return clone

    def _ln(self) -> 'SimpleNumber':
        """Estimate the natural logarithm of a simple number."""
        sn = SimpleNumber(0)
        for k in range(0, 4):
            # 2k + 1
            common = SimpleNumber(k).binary('mul', SimpleNumber(2)).binary('add', SimpleNumber(1))
            # 1 / (2k + 1)
            lsn = SimpleNumber(1).binary('div', common)
            # ((z - 1) / (z + 1))^(2k + 1)
            num = self.binary('sub', SimpleNumber(1))
            denom = self.binary('add', SimpleNumber(1))
            rsn = num.binary('div', denom).binary('exp', common)
            # add product of terms
            sn = sn.binary('add', lsn.binary('mul', rsn))
        sn = sn.binary('mul', SimpleNumber(2))
        return sn

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

    def assign(self, num_index: int) -> Tuple[Node, 'SimpleNumber']:
        """Generate a YOLOL assignment statement."""
        ident = 'n{}'.format(num_index)
        var = Node(kind='variable', value=ident)
        expr = self.evaluate()
        asn = Node(kind='assignment', children=[var, expr])
        return asn, SimpleNumber(ident)
