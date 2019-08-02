from copy import deepcopy
from typing import Union, Any, Tuple, List

from engine.node import Node


class Number:
    """Represents a number, variable, or external."""
    PREFIX = '_yovec_num'

    def __init__(self, n: Union[int, float, str]):
        self.initial = n
        self.queue = []

    @property
    def class_name(self):
        return 'number'

    # Operations

    def unary(self, op: str) -> 'Number':
        """Apply a unary operation to a number."""
        clone = deepcopy(self)
        clone.queue.append((op,))
        return clone

    def binary(self, op: str, other: 'Number') -> 'Number':
        """Apply a binary operation to a number."""
        clone = deepcopy(self)
        clone.queue.append((op, other))
        return clone

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

    def assign(self, index: int) -> Tuple[List[Node], 'Number']:
        """Generate YOLOL assignment statements."""
        ident = '{}{}'.format(Number.PREFIX, index)
        var = Node(kind='variable', value=ident)
        expr = self.evaluate()
        asn = Node(kind='assignment', children=[var, expr])
        return [asn], Number(ident)
