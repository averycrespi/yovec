from copy import deepcopy
from typing import List, Tuple

from engine.errors import YovecError
from engine.node import Node
from engine.number import SimpleNumber
from engine.vector import SimpleVector



class SimpleMatrix:
    """Represents a list of simple vectors."""
    def __init__(self, svecs: List[SimpleVector]):
        assert len(svecs) > 0
        if len(svecs) > 1:
            n = svecs[0].length
            for sv in svecs[1:]:
                if sv.length != n:
                    raise YovecError('all vectors in a matrix must have the same length')
        self.svecs = svecs
        self._rows = len(self.svecs)
        self._cols = self.svecs[0].length

    # Operations

    def matbinary(self, op: str, other: 'SimpleMatrix') -> 'SimpleMatrix':
        """Apply a binary operation to two simple matrices."""
        if self._rows != other._rows or self._cols != other._cols:
            raise YovecError('cannot apply operation "{}" to matrices of different sizes'.format(op))
        return SimpleMatrix([sv.vecbinary(op.replace('mat_', 'vec_'), other.svecs[i]) for i, sv in enumerate(self.svecs)])

    def map(self, op: str) -> 'SimpleMatrix':
        """Map a unary operation to a simple matrix."""
        return SimpleMatrix([sv.map(op) for sv in self.svecs])

    def premap(self, op: str, other: SimpleNumber) -> 'SimpleMatrix':
        """Premap a binary operation to a simple matrix."""
        svecs = []
        for sv in self.svecs:
            svecs.append(SimpleVector([sn.binary(op, other) for sn in sv.snums]))
        return SimpleMatrix(svecs)

    def postmap(self, other: SimpleNumber, op: str) -> 'SimpleMatrix':
        """Postmap a binary operation to a simple matrix."""
        svecs = []
        for sv in self.svecs:
            svecs.append(SimpleVector([other.binary(op, sn) for sn in sv.snums]))
        return SimpleMatrix(svecs)

    def transpose(self) -> 'SimpleMatrix':
        """Return the transpose of the simple matrix."""
        svecs = []
        for i in range(self._cols):
            svecs.append(SimpleVector([sv.snums[i] for sv in self.svecs]))
        return SimpleMatrix(svecs)

    def matmul(self, other: 'SimpleMatrix') -> 'SimpleMatrix':
        """Multiply two simple matrices."""
        if self._cols != other._rows:
            raise YovecError('cannot mulitply matrices with mismatching sizes')
        svecs = []
        for i in range(self._rows):
            snums = []
            for j in range(other._cols):
                sn = SimpleNumber(0)
                for k in range(other._rows):
                    sn = sn.binary('add', self.svecs[i].snums[k].binary('mul', other.svecs[k].snums[j]))
                snums.append(sn)
            svecs.append(SimpleVector(snums))
        return SimpleMatrix(svecs)

    def rows(self) -> SimpleNumber:
        """Return the number of rows in the simple matrix."""
        return SimpleNumber(self._rows)

    def cols(self) -> SimpleNumber:
        """Return the number of columns in the simple matrix."""
        return SimpleNumber(self._cols)

    # Resolutions

    def assign(self, mat_index: int) -> Tuple[List[Node], 'SimpleMatrix']:
        """Generate YOLOL assignment statements."""
        assignments = []
        svecs = []
        for i, sv in enumerate(self.svecs):
            snums = []
            for j, sn in enumerate(sv.snums):
                expr = sn.evaluate()
                ident = 'm{}r{}c{}'.format(mat_index, i, j)
                var = Node(kind='variable', value=ident)
                asn = Node(kind='assignment', children=[var, expr])
                assignments.append(asn)
                snums.append(SimpleNumber(ident))
            svecs.append(SimpleVector(snums))
        return assignments, SimpleMatrix(svecs)
