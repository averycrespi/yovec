from copy import deepcopy
from typing import List, Tuple

from engine.node import Node
from engine.number import SimpleNumber


class SimpleVector:
    """Represents a list of simple numbers."""
    def __init__(self, snums: List[SimpleNumber]):
        self.initial = snums
        self.length = len(self.initial)
        self.queue = []

    # Operations

    def vecunary(self, op: str) -> 'SimpleVector':
        """Apply a unary operation to a simple vector."""
        result = deepcopy(self)
        result.queue.append((op,))
        return result

    def vecbinary(self, op: str, sv: 'SimpleVector') -> 'SimpleVector':
        """Apply a binary operation to two simple vectors."""
        if self.length != sv.length:
            raise ValueError('cannot apply operation {} to vectors of different lengths'.format(op))
        result = deepcopy(self)
        result.queue.append((op, sv))
        return result

    def map(self, op: str) -> 'SimpleVector':
        """Map a unary operation to a simple vector."""
        result = deepcopy(self)
        result.queue.append(('vec_map', op))
        return result

    def premap(self, op: str, sn: SimpleNumber) -> 'SimpleVector':
        """Premap a binary operation to a simple vector."""
        result = deepcopy(self)
        result.queue.append(('vec_premap', op, sn))
        return result

    def postmap(self, sn: SimpleNumber, op: str) -> 'SimpleVector':
        """Postmap a binary operation to a simple vector."""
        result = deepcopy(self)
        result.queue.append(('vec_postmap', sn, op))
        return result

    def concat(self, sv: 'SimpleVector') -> 'SimpleVector':
        """Concatenate two simple vectors."""
        initial = [*self.resolve(), *sv.resolve()]
        return SimpleVector(initial)

    def dot(self, sv: 'SimpleVector') -> SimpleNumber:
        """Calculate the dot product of two simple vectors."""
        result = SimpleNumber(0)
        for lsn, rsn in zip(self.resolve(), sv.resolve()):
            result = result.binary('add', lsn.binary('mul', rsn))
        return result

    def len(self) -> SimpleNumber:
        """Return the length of the simple vector."""
        return SimpleNumber(self.length)

    def reduce(self, op: str) -> SimpleNumber:
        """Reduce the simple vector to a simple number."""
        snums = self.resolve()
        result = snums[0]
        for sn in snums[1:]:
            result = result.binary(op, sn)
        return result

    # Resolutions

    def resolve(self) -> List[SimpleNumber]:
        """Resolve operations for each simple number."""
        results = []
        for i, sn in enumerate(self.initial):
            for op, *args in self.queue:
                if op == 'vec_map':
                    sn = sn.unary(args[0])
                elif op == 'vec_premap':
                    sn = sn.binary(args[0], args[1])
                elif op == 'vec_postmap':
                    sn = args[0].binary(args[1], sn)
                elif len(args) == 0: # unary
                    sn = sn.unary(op.strip('vec_'))
                elif len(args) == 1: # binary
                    sn = sn.binary(op.strip('vec_'), args[0].resolve()[i])
                else:
                    raise ValueError('unrecognized item in queue: {}, {}'.format(op, args))
            results.append(sn)
        return results

    def assign(self, index: int) -> Tuple[List[Node], 'SimpleVector']:
        """Generate YOLOL assignment statements."""
        assignments = []
        snums = []
        expressions = [sn.evaluate() for sn in self.resolve()]
        for i, expr in enumerate(expressions):
            ident = 'v{}e{}'.format(index, i)
            var = Node(kind='variable', value=ident)
            asn = Node(kind='assignment', children=[var, expr])
            assignments.append(asn)
            snums.append(SimpleNumber(ident))
        return assignments, SimpleVector(snums)
