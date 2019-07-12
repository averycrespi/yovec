from typing import Tuple

from engine.node import Node
from engine.optimize.decimal import Decimal

from engine.errors import YovecError


def reduce_expressions(program: Node) -> Node:
    """Reduce expressions in a YOLOL program."""
    assert program.kind == 'program'
    clone = program.clone()
    delta = True
    while delta:
        clone, fold_delta = _fold_constants(clone)
        delta = fold_delta
    return clone


def _fold_constants(program: Node) -> Tuple[Node, bool]:
    """Fold constants."""
    assert program.kind == 'program'
    clone = program.clone()
    numbers = clone.find(lambda node: node.kind == 'number')
    for num in numbers:
        assert num.parent is not None
        if len(num.parent.children) == 2: # type: ignore
            if _fold_binary(num.parent): # type: ignore
                return clone, True
    return clone, False


def _fold_binary(expr: Node):
    """Fold constants in a binary operation."""
    assert len(expr.children) == 2 and expr.parent is not None
    left, right = expr.children
    delta = False
    replacement = None
    if expr.kind == 'add' and left.value == 0:
        # 0 + n => n
        delta = True
        replacement = right
    elif expr.kind == 'add' and right.value == 0:
        # n + 0 => n
        delta = True
        replacement = left
    elif expr.kind == 'sub' and right.value == 0:
        # n - 0 => n
        delta = True
        replacement = left
    elif expr.kind == 'mul' and left.value == 0:
        # 0 * n => 0
        delta = True
        replacement = Node(kind='number', value=0)
    elif expr.kind == 'mul' and right.value == 0:
        # n * 0 => 0
        delta = True
        replacement = Node(kind='number', value=0)
    elif expr.kind == 'mul' and left.value == 1:
        # 1 * n => n
        delta = True
        replacement = right
    elif expr.kind == 'mul' and right.value == 1:
        # n * 1 => n
        delta = True
        replacement = left
    elif expr.kind == 'div' and right.value == 1:
        # n / 1 => n
        delta = True
        replacement = left
    elif expr.kind == 'exp' and left.value == 1:
        # 1 ^ n = >
        delta = True
        replacement = left
    elif expr.kind == 'exp' and right.value == 1:
        # n ^ 1 => n
        delta = True
        replacement = left
    elif left.kind == 'number' and right.kind == 'number':
        try:
            delta = True
            result = str(Decimal(left.value).binary(expr.kind, Decimal(right.value)))
            replacement = Node(kind='number', value=result)
        except ArithmeticError:
            raise YovecError('failed to fold constants in expression: {}'.format(expr))
    if delta:
        expr.parent.remove_child(expr)
        expr.parent.append_child(replacement)
        return True
    else:
        return False
