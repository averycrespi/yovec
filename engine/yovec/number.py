from copy import deepcopy
from typing import Union

from engine.node import Node


class SimpleNumber:
    """Represents a number or external."""
    def __init__(self, n: Union[int, str]):
        self.initial = n
        self.opqueue = []

    # Operations

    def unary(self, op: str) -> 'SimpleNumber':
        """Apply a unary operation to a simple number."""
        result = deepcopy(self)
        result.opqueue.append((op,))
        return result

    def binary(self, op: str, sn: 'SimpleNumber') -> 'SimpleNumber':
        """Apply a binary operation to a simple number."""
        result = deepcopy(self)
        result.opqueue.append((op, sn))
        return result

    # Resolutions

    def evaluate(self) -> Node:
        """Generate a YOLOL expression."""
        pass #TODO: implement
