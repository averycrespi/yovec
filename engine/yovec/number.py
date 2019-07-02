from typing import Union

from engine.node import Node


class SimpleNumber:
    """Represents a number or external."""
    def __init__(self, n: Union[int, str]):
        self.n = n
        self.queue = []

    # Enqueues

    def unary(self, op: str): self.queue.append((op,))
    def binary(self, op:str, sn: 'SimpleNumber'): self.queue.append((op, sn))

    # Resolutions

    def evaluate(self) -> Node:
        """Generate a YOLOL expression."""
        pass #TODO: implement
