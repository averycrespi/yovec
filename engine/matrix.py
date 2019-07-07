from copy import deepcopy
from typing import List, Tuple

from engine.errors import YovecError
from engine.node import Node
from engine.number import Number
from engine.vector import Vector



class Matrix:
    """Represents a list of vectors."""
    def __init__(self, vecs: List[Vector]):
        assert len(vecs) > 0
        if len(vecs) > 1:
            for v in vecs[1:]:
                if v.length != vecs[0].length:
                    raise YovecError('all vectors in a matrix must have the same length')
        self.vecs = vecs
        self._rows = len(self.vecs)
        self._cols = self.vecs[0].length

    # Operations

    def matbinary(self, op: str, other: 'Matrix') -> 'Matrix':
        """Apply a binary operation to two matrices."""
        if self._rows != other._rows or self._cols != other._cols:
            raise YovecError('cannot apply operation "{}" to matrices of different sizes'.format(op))
        return Matrix([v.vecbinary(op.replace('mat_', 'vec_'), other.vecs[i]) for i, v in enumerate(self.vecs)])

    def map(self, op: str) -> 'Matrix':
        """Map a unary operation to a matrix."""
        return Matrix([v.map(op) for v in self.vecs])

    def premap(self, op: str, other: Number) -> 'Matrix':
        """Premap a binary operation to a matrix."""
        vecs = []
        for v in self.vecs:
            vecs.append(Vector([n.binary(op, other) for n in v.nums]))
        return Matrix(vecs)

    def postmap(self, other: Number, op: str) -> 'Matrix':
        """Postmap a binary operation to a matrix."""
        vecs = []
        for v in self.vecs:
            vecs.append(Vector([other.binary(op, n) for n in v.nums]))
        return Matrix(vecs)

    def apply(self, op: str, other: 'Matrix') -> 'Matrix':
        """Apply a binary operation to two matrices."""
        if self._rows != other._rows or self._cols != other._cols:
            raise YovecError('cannot apply operation "{}" to matrices of different sizes'.format(op))
        return Matrix([lv.apply(op, rv) for lv, rv in zip(self.vecs, other.vecs)])

    def transpose(self) -> 'Matrix':
        """Return the transpose of the matrix."""
        vecs = []
        for i in range(self._cols):
            vecs.append(Vector([v.nums[i] for v in self.vecs]))
        return Matrix(vecs)

    def matmul(self, other: 'Matrix') -> 'Matrix':
        """Multiply two matrices."""
        if self._cols != other._rows:
            raise YovecError('cannot mulitply matrices with mismatching sizes')
        vecs = []
        for i in range(self._rows):
            nums = []
            for j in range(other._cols):
                n = Number(0)
                for k in range(other._rows):
                    n = n.binary('add', self.vecs[i].nums[k].binary('mul', other.vecs[k].nums[j]))
                nums.append(n)
            vecs.append(Vector(nums))
        return Matrix(vecs)

    def rows(self) -> Number:
        """Return the number of rows in the matrix."""
        return Number(self._rows)

    def cols(self) -> Number:
        """Return the number of columns in the matrix."""
        return Number(self._cols)

    # Resolutions

    def assign(self, index: int) -> Tuple[List[Node], 'Matrix']:
        """Generate YOLOL assignment statements."""
        assignments = []
        vecs = []
        for i, v in enumerate(self.vecs):
            nums = []
            for j, n in enumerate(v.nums):
                expr = n.evaluate()
                ident = 'm{}r{}c{}'.format(index, i, j)
                var = Node(kind='variable', value=ident)
                asn = Node(kind='assignment', children=[var, expr])
                assignments.append(asn)
                nums.append(Number(ident))
            vecs.append(Vector(nums))
        return assignments, Matrix(vecs)
