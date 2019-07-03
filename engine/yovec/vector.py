from copy import deepcopy
from typing import List

from engine.node import Node
from engine.yovec.number import SimpleNumber


class SimpleVector:
    """Represents a list of simple numbers."""
    def __init__(self, snums: List[SimpleNumber]):
        self.initial = snums
        self.opqueue = []

    def vecunary(self, op: str) -> 'SimpleVector':
        """Apply a unary operation to a simple vector."""
        result = deepcopy(self)
        result.opqueue.append((op,))
        return result

    def vecbinary(self, op: str, sv: 'SimpleVector') -> 'SimpleVector':
        """Apply a binary operation to two simple vectors."""
        result = deepcopy(self)
        result.opqueue.append((op, sv))
        return result

    def premap(self, op: str, sn: SimpleNumber) -> 'SimpleVector':
        """Premap an operation to a simple vector."""
        result = deepcopy(self)
        result.opqueue.append(('premap', op, sn))
        return result

    def postmap(self, sn: SimpleNumber, op: str): -> 'SimpleVector':
        """Postmap an operation to a simple vector."""
        result = deepcopy(self)
        result.opqueue.append(('postmap', sn, op))
        return result

    def dot(self, sv: 'SimpleVector') -> SimpleNumber:
        """Calculate the dot product of two simple vectors."""
        lsnums = None #TODO: apply ops element-wise
        rsnums = None #TODO: apply ops element-wise
        result = SimpleNumber(0)
        for lsn, rsn in zip(left_snums, right_snums):
            result = result.add(lsn.mul(rsn))
        return result

    def len(self) -> SimpleNumber:
        """Return the length of the simple vector."""
        return len(self.snums)

    def reduce(self, op: str) -> SimpleNumber:
        """Reduce the simple vector to a simple number."""
        snums = None #TODO: apply ops element-wise
        result = snums[0]
        for sn in snums[1:]:
            result = result.binary(op, sn)
        return result

    def assign(self, index: int) -> List[Node]:
        """Generate YOLOL assignment statements."""
        pass #TODO: implement
