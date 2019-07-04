from copy import deepcopy
from typing import List, Tuple

from engine.errors import YovecError
from engine.node import Node
from engine.number import SimpleNumber



class SimpleVector:
    """Represents a list of simple numbers."""
    def __init__(self, snums: List[SimpleNumber]):
        self.snums = snums
        self.length = len(snums)

    # Operations

    def vecunary(self, op: str) -> 'SimpleVector':
        """Apply a unary operation to a simple vector."""
        return SimpleVector([sn.unary(op.strip('vec_')) for sn in self.snums])

    def vecbinary(self, op: str, other: 'SimpleVector') -> 'SimpleVector':
        """Apply a binary operation to two simple vectors."""
        if self.length != other.length:
            raise YovecError('cannot apply operation "{}" to vectors of different lengths'.format(op))
        return SimpleVector([sn.binary(op.strip('vec_'), other.snums[i]) for i, sn in enumerate(self.snums)])

    def map(self, op: str) -> 'SimpleVector':
        """Map a unary operation to a simple vector."""
        return SimpleVector([sn.unary(op) for sn in self.snums])

    def premap(self, op: str, other: SimpleNumber) -> 'SimpleVector':
        """Premap a binary operation to a simple vector."""
        return SimpleVector([sn.binary(op, other) for sn in self.snums])

    def postmap(self, other: SimpleNumber, op: str) -> 'SimpleVector':
        """Postmap a binary operation to a simple vector."""
        return SimpleVector([other.binary(op, sn) for sn in self.snums])

    def concat(self, other: 'SimpleVector') -> 'SimpleVector':
        """Concatenate two simple vectors."""
        return SimpleVector([*self.snums, *other.snums])

    def dot(self, other: 'SimpleVector') -> SimpleNumber:
        """Calculate the dot product of two simple vectors."""
        sn = SimpleNumber(0)
        for lsn, rsn in zip(self.snums, other.snums):
            sn = sn.binary('add', lsn.binary('mul', rsn))
        return sn

    def len(self) -> SimpleNumber:
        """Return the length of the simple vector."""
        return SimpleNumber(self.length)

    def reduce(self, op: str) -> SimpleNumber:
        """Reduce the simple vector to a simple number."""
        lsn = self.snums[0]
        for rsn in self.snums[1:]:
            lsn = lsn.binary(op, rsn)
        return lsn

    # Resolutions

    def assign(self, vec_index: int) -> Tuple[List[Node], 'SimpleVector']:
        """Generate YOLOL assignment statements."""
        assignments = []
        snums = []
        expressions = [sn.evaluate() for sn in self.snums]
        for i, expr in enumerate(expressions):
            ident = 'v{}e{}'.format(vec_index, i)
            var = Node(kind='variable', value=ident)
            asn = Node(kind='assignment', children=[var, expr])
            assignments.append(asn)
            snums.append(SimpleNumber(ident))
        return assignments, SimpleVector(snums)
