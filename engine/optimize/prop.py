from engine.node import Node
from engine.optimize.decimal import Decimal

from engine.errors import YovecError


def propagate_constants(program: Node) -> Node:
    """Propagate constants in a YOLOL program."""
    assert program.kind == 'program'
    clone = program.clone()
    delta = True
    while delta:
        delta = False
        numbers = clone.find(lambda node: node.kind == 'number')
        for num in numbers:
            assert num.parent is not None
            if len(num.parent.children) == 2 and all(c.kind == 'number' for c in num.parent.children):
                _propagate_binary(num.parent)
                delta = True
                break
    return clone


def _propagate_binary(expr: Node):
    """Propagate constants in a binary operation."""
    assert len(expr.children) == 2
    try:
        result = Decimal(expr.children[0].value).binary(expr.kind, Decimal(expr.children[1].value))
    except ArithmeticError:
        raise YovecError('failed to propagate constants for expression: {}'.format(expr))
    assert expr.parent is not None
    expr.parent.remove_child(expr)
    expr.parent.append_child(Node(kind='number', value=str(result)))
