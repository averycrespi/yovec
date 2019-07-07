from copy import deepcopy
from typing import List, Tuple

from engine.errors import YovecError
from engine.node import Node
from engine.number import Number



class Vector:
    """Represents a list of numbers."""
    def __init__(self, nums: List[Number]):
        self.nums = nums
        self.length = len(nums)

    # Operations

    def vecbinary(self, op: str, other: 'Vector') -> 'Vector':
        """Apply a binary operation to two vectors."""
        if self.length != other.length:
            raise YovecError('cannot apply operation "{}" to vectors of different lengths'.format(op))
        return Vector([n.binary(op.strip('vec_'), other.nums[i]) for i, n in enumerate(self.nums)])

    def map(self, op: str) -> 'Vector':
        """Map a unary operation to a vector."""
        return Vector([n.unary(op) for n in self.nums])

    def premap(self, op: str, other: Number) -> 'Vector':
        """Premap a binary operation to a vector."""
        return Vector([n.binary(op, other) for n in self.nums])

    def postmap(self, other: Number, op: str) -> 'Vector':
        """Postmap a binary operation to a vector."""
        return Vector([other.binary(op, n) for n in self.nums])

    def apply(self, op: str, other: 'Vector') -> 'Vector':
        """Apply a binary operation to two vectors."""
        if self.length != other.length:
            raise YovecError('cannot apply operation "{}" to vectors of different lengths'.format(op))
        return Vector([ln.binary(op, rn) for ln, rn in zip(self.nums, other.nums)])

    def concat(self, other: 'Vector') -> 'Vector':
        """Concatenate two vectors."""
        return Vector([*self.nums, *other.nums])

    def reverse(self) -> 'Vector':
        """Reverse a vector."""
        return Vector(list(self.nums[::-1]))

    def dot(self, other: 'Vector') -> Number:
        """Calculate the dot product of two vectors."""
        n = Number(0)
        for ln, rn in zip(self.nums, other.nums):
            n = n.binary('add', ln.binary('mul', rn))
        return n

    def len(self) -> Number:
        """Return the length of the vector."""
        return Number(self.length)

    def reduce(self, op: str) -> Number:
        """Reduce the vector to a number."""
        ln = self.nums[0]
        for rn in self.nums[1:]:
            ln = ln.binary(op, rn)
        return ln

    # Resolutions

    def assign(self, index: int) -> Tuple[List[Node], 'Vector']:
        """Generate YOLOL assignment statements."""
        assignments = []
        nums = []
        expressions = [n.evaluate() for n in self.nums]
        for i, expr in enumerate(expressions):
            ident = 'v{}e{}'.format(index, i)
            var = Node(kind='variable', value=ident)
            asn = Node(kind='assignment', children=[var, expr])
            assignments.append(asn)
            nums.append(Number(ident))
        return assignments, Vector(nums)
