from copy import deepcopy
from typing import List

from engine.node import Node
from engine.yovec.number import SimpleNumber


class SimpleVector:
    """Represents a list of simple numbers."""
    def __init__(self, snums: List[SimpleNumber]):
        self.initial = snums
        self.opqueue = []

    # Operations

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

    def postmap(self, sn: SimpleNumber, op: str) -> 'SimpleVector':
        """Postmap an operation to a simple vector."""
        result = deepcopy(self)
        result.opqueue.append(('postmap', sn, op))
        return result

    def dot(self, sv: 'SimpleVector') -> SimpleNumber:
        """Calculate the dot product of two simple vectors."""
        result = SimpleNumber(0)
        for lsn, rsn in zip(self.resolve(), sv.resolve()):
            result = result.add(lsn.mul(rsn))
        return result

    def len(self) -> SimpleNumber:
        """Return the length of the simple vector."""
        return SimpleNumber(len(self.snums))

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
        for sn in self.initial:
            for event in self.opqueue:
                if event[0] == 'premap':
                    sn = sn.binary(event[1], event[2])
                elif event[0] == 'postmap':
                    sn = event[1].binary(event[2], sn)
                elif len(event) == 1:
                    sn = sn.unary(event[0])
                elif len(event) == 2:
                    sn = sn.binary(event[0], event[1])
                else:
                    raise ValueError('unrecognized event: {}'.format(event))
            results.append(sn)
        return results

    def assign(self, index: int) -> List[Node]:
        """Generate YOLOL assignment statements."""
        assignments = []
        expressions = [sn.evaluate() for sn in self.resolve()]
        for i, expr in enumerate(expressions):
            #TODO: add subnode to variable?
            var = Node(kind='variable', value='v{}e{}'.format(index, i))
            asn = Node(kind='assignment', children=[var, expr])
            assignments.append(a)
        return assignments
