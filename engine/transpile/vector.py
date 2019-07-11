from copy import deepcopy
from typing import Sequence, Union

from engine.errors import YovecError
from engine.transpile.number import Number


class Vector:
    """Represents an N-dimensional vector."""
    def __init__(self, elems: Union[Sequence['Vector'], Number]):
        if type(elems) == Number:
            self.number = elems
            self.vectors = None
            self.dim = 0
            self.length = 1
        elif len({v.length for v in elems}) != 1:
            raise YovecError('cannot create vector with multiple lengths')
        elif len({v.dim for v in elems}) != 1:
            raise YovecError('cannot create vector with multiple dimensionalities')
        else:
            self.numbers = None
            self.vectors = elems
            self.dim = elems[0].dim + 1
            self.length = len(elems)

    def map_unary(self, op: str) -> 'Vector':
        """Map a unary operation onto an N-dimensional vector.

        Returns an N-dimensional vector.
        """
        if self.vectors is None:
            return Vector(self.number.unary(op))
        else:
            return Vector([v.map_unary(op) for v in self.vectors])

    def map_binary(self, op: str, other: 'Vector') -> 'Vector':
        """Map a binary operation onto two N-dimensional vectors.

        Both vectors must have the same length and dimensionality.

        Returns an N-dimensional vector.
        """
        if self.dim != other.dim:
            raise YovecError('cannot apply operation {} to vectors with different dimensionalities'.format(op))
        elif self.length != other.length:
            raise YovecError('cannot apply operation {} to vectors with different lengths'.format(op))
        elif self.vectors is None:
            return Vector(self.number.binary(op, other.number.binary))
        else:
            return Vector([v.map_binary(op, o) for v, o in zip(self.vectors, other.vectors)])

    def concat(self, other: 'Vector') -> 'Vector':
        """Shallowly concatenate two (N>0)-dimensional vectors.

        Both vectors must have the same dimensionality.

        Returns an N-dimensional vector.
        """
        if self.dim != other.dim:
            raise YovecError('cannot concatenate vectors with different dimensionalities')
        elif self.vectors is None:
            raise YovecError('cannot concatenate 0-dimensional vectors')
        else:
            return Vector([*self.vectors, *other.vectors])

    def dot(self, other: 'Vector') -> 'Vector':
        """Calculate the dot product of two 1-dimensional vectors.

        Both vectors must have the same length.

        Returns a 0-dimensional vector.
        """
        if self.dim != 1 or other.dim != 1:
            raise YovecError('can only calculate dot product of 1-dimensional vectors')
        elif self.length != other.length:
            raise YovecError('cannot calculate dot product of vectors with different lengths')
        n = Number(0)
        lns = [v.number for v in self.vectors]
        rns = [v.number for v in other.vectors]
        for ln, rn in zip(lns, rns):
            n = n.binary('add', ln.binary('mul', rn))
        return Vector(n)

    def elem(self, lit: str) -> 'Vector':
        """Get an element from an (N>0)-dimensional vector.

        Returns an (N-1)-dimensional vector.
        """
        pass #TODO

    def matmul(self, other: 'Vector') -> 'Vector':
        """Multiply two 2-dimensional vectors.

        Returns a 2-dimensional vector.
        """
        pass #TODO

    def reduce(self, op: str) -> 'Vector':
        """Reduce an N-dimensional vector.

        Returns a 0-dimensional vector.
        """
        if self.vectors is None:
            return Vector(self.number)
        pass #TODO

    def repeat(self, lit: str) -> 'Vector':
        """Repeat an N-dimensional vector.

        Returns a (N+1)-dimensional vector.
        """
        try:
            count = int(lit)
        except ValueError:
            raise YovecError('invalid count: {}'.format(lit))
        if count <= 0:
            raise YovecError('count must be positive: {}'.format(count))
        elif self.vectors is None:
            return Vector([self.number] * count)
        else:
            return Vector([self.vectors] * count)

    def reverse(self) -> 'Vector':
        """Shallowly reverse an N-dimensional vector.

        Returns an N-dimensional vector.
        """
        if self.vectors is None:
            return Vector(self.number)
        else:
            return Vector(self.vectors[::-1])

    def transpose(self) -> 'Vector':
        """Swap the rows and columns of a 2-dimensional vector.

        Returns a 2-dimensional vector.
        """
        pass #TODO

    # Operations

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
