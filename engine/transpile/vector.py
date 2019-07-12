from copy import deepcopy
from typing import Sequence, Union, Tuple, List, Optional

from engine.errors import YovecError
from engine.node import Node
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
        if self.dim == 0:
            return Vector(self.number.unary(op))
        else:
            return Vector([v.map_unary(op) for v in self.vectors])

    def map_binary(self, op: str, other: 'Vector') -> 'Vector':
        """Map a binary operation onto two N-dimensional vectors.

        Both vectors must have the same length and dimensionality.

        Returns an N-dimensional vector.
        """
        if self.dim != other.dim:
            raise YovecError('cannot apply operation {} to vectors with different dimensionalities: {}, {}'.format(op, self.dim, other.dim))
        elif self.length != other.length:
            raise YovecError('cannot apply operation {} to vectors with different lengths'.format(op))
        elif self.dim == 0:
            return Vector(self.number.binary(op, other.number))
        else:
            return Vector([v.map_binary(op, o) for v, o in zip(self.vectors, other.vectors)])

    def concat(self, other: 'Vector') -> 'Vector':
        """Shallowly concatenate two (N>0)-dimensional vectors.

        Both vectors must have the same dimensionality.

        Returns an N-dimensional vector.
        """
        if self.dim != other.dim:
            raise YovecError('cannot concatenate vectors with different dimensionalities')
        elif self.dim == 0:
            raise YovecError('cannot concatenate 0-dimensional vectors')
        else:
            return Vector([*self.vectors, *other.vectors])

    def dim(self) -> 'Vector':
        """Get the dimensionality of an N-dimensional version.

        Returns a 0-dimensional vector.
        """
        return Vector(self.dim)

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
        try:
            index = int(lit)
        except ValueError:
            raise YovecError('invalid index: {}'.format(lit))
        if index < 0 or index >= self.length:
            raise YovecError('index is out of range: {}'.format(index))
        elif self.dim == 0:
            raise YovecError('cannot get element from a 0-dimensional vector')
        else:
            return Vector(self.vectors[index])

    def len(self) -> 'Vector':
        """Get the length of an N-dimensional vector.

        Returns a 0-dimensional vector.
        """
        return Vector(self.length)

    def matmul(self, other: 'Vector') -> 'Vector':
        """Multiply two 2-dimensional vectors.

        Returns a 2-dimensional vector.
        """
        if self.dim != 2 or other.dim != 2:
            raise YovecError('can only calculate matrix product of 2-dimensional vectors')
        self_cols = self.vectors[0].length
        self_rows = self.length
        other_cols = other.vectors[0].length
        other_rows = other.length
        if self_cols != other_rows:
            raise YovecError('cannot multiple matrices with mismatching sizes')
        vectors = []
        for i in range(self_rows):
            numbers = []
            for j in range(other_cols):
                n = Number(0)
                for k in range(other_rows):
                    n = n.binary('add', self.vectors[i].vectors[k].binary('mul', other.vectors[k].vectors[j]))
                numbers.append(Vector(n))
            vectors.append(numbers)
        return Vector(vectors)

    def reduce(self, op: str) -> 'Vector':
        """Reduce an (N>0)-dimensional vector.

        Returns a 0-dimensional vector.
        """
        if self.dim == 0:
            raise YovecError('cannot reduce a 0-dimensional vector')
        elif self.dim == 1:
            n = self.vectors[0].number
            for vec in self.vectors[1:]:
                n = n.binary(op, vec.number)
            return Vector(n)
        else:
            return Vector([v.reduce(op) for v in self.vectors])

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
        if self.dim != 2:
            raise YovecError('can only transpose 2-dimensional vector')
        vectors = []
        cols = self.vectors[0].length
        for i in range(cols):
            vectors.append(Vector([v.vectors[i] for v in self.vectors]))
        return Vector(vectors)

    def assign(self, prefix: str, indices: Optional[Tuple[str]]=None) -> Tuple[List[Node], 'Vector']:
        """Generate YOLOL assignment statements from an N-dimensional vector."""
        if indices is None:
            indices = (prefix,)
        if self.dim == 0:
            expr = self.number.evaluate()
            ident = '_'.join(i for i in indices)
            var = Node(kind='variable', value=ident)
            asn = Node(kind='assignment', children=[var, expr])
            return [asn], Vector(Number(ident))
        else:
            vectors = []
            assignments = []
            for i, v in enumerate(self.vectors):
                asns, vec = v.assign(prefix, indices=(*indices, str(i)))
                assignments.extend(asns)
                vectors.append(vec)
            return assignments, Vector(vectors)
