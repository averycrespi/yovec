from typing import List

from engine.node import Node
from engine.yovec.number import SimpleNumber



class SimpleVector:
    """Represents a list of simple numbers."""
    def __init__(self, snums: List[SimpleNumber]):
        self.snums = snums
        self.queue = []

    # Enqueues

    def vecunary(self, op: str): self.queue.append((op,))
    def vecbinary(self, op: str, sv: 'SimpleVector'): self.queue.append((op, sv))
    def premap(self, op: str, sn: SimpleNumber): self.queue.append(('premap', op, sn))
    def postmap(self, op: str, sn: SimpleNumber): self.queue.append(('postmap', op, sn))

    # Resolutions

    def dot(self) -> SimpleNumber:
        """Calculate the dot product of the simple vector."""
        pass #TODO: implement

    def cross(self) -> SimpleNumber:
        """Calculate the cross product of the simple vector."""
        pass #TODO: implement

    def len(self) -> SimpleNumber:
        """Return the length of the simple vector."""
        return SimpleNumber(len(self.snums))

    def reduce(self, op: str) -> SimpleNumber:
        """Reduce the simple vector to a simple number."""
        pass #TODO: implement

    def concat(self, sv: 'SimpleVector') -> 'SimpleVector':
        """Concatenate two simple vectors."""
        pass #TODO: implement

    def assign(self, vindex: int) -> List[Node]:
        """Generate YOLOL assignments."""
        pass #TODO: implement
