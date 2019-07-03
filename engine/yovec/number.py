from copy import deepcopy
from typing import Union, Any

from engine.node import Node


class SimpleNumber:
    """Represents a number or external."""
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
        #TODO: implement
        return Node(kind='TODO', value=self.queue)
