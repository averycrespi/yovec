from copy import deepcopy
from typing import Union, Any

from engine.node import Node


class SimpleNumber:
    """Represents a number, variable, or external."""
    def __init__(self, n: Union[int, float, str]):
        self.initial = n
        self.queue = []

    # Operations

    def unary(self, op: str) -> 'SimpleNumber':
        """Apply a unary operation to a simple number."""
        result = deepcopy(self)
        result.queue.append((op,))
        return result

    def binary(self, op: str, sn: 'SimpleNumber') -> 'SimpleNumber':
        """Apply a binary operation to a simple number."""
        result = deepcopy(self)
        result.queue.append((op, sn))
        return result

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
