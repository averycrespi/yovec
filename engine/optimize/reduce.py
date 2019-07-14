from engine.node import Node
from engine.optimize.decimal import Decimal

from engine.errors import YovecError


def reduce_expressions(program: Node) -> Node:
    """Reduce expressions in a YOLOL program."""
    assert program.kind == 'program'
    clone = program.clone()
    while _propagate_constants(clone) or _fold_constants(clone):
        pass
    return clone


def _propagate_constants(program: Node) -> bool:
    """Propagate constants in a program."""
    assert program.kind == 'program'
    variables = program.find(lambda node: node.kind == 'variable')
    for var in variables:
        # Ignore "A" in "let number A = B"
        if var.parent.kind == 'assignment' and var.parent.children.index(var) == 0:
            continue
        if _propagate_var(program, var):
            return True
    return False


def _propagate_var(program: Node, var: Node):
    "Propagate constants in an variable."
    # Look for "let number A = B" with a given "A"
    assignments = program.find(lambda node: node.kind == 'assignment' and node.children[0].value == var.value)
    if len(assignments) == 0:
        # Found external
        return False
    expr = assignments[0].children[1].clone()
    # Check if expr is constant
    if len(expr.find(lambda node: node.kind == 'variable')) == 0:
        var.parent.append_child(expr)
        var.parent.remove_child(var)
        return True
    return False


def _fold_constants(program: Node) -> bool:
    """Fold constants in a program."""
    assert program.kind == 'program'
    numbers = program.find(lambda node: node.kind == 'number')
    for num in numbers:
        if len(num.parent.children) == 2 and _fold_binary_expr(num.parent):
            return True
    return False


def _fold_binary_expr(expr: Node):
    """Fold constants in a binary expression."""
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
    elif expr.kind == 'mul' and left.value == 0 or right.value == 0:
        # 0 * n => 0
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
        expr.parent.append_child(replacement)
        expr.parent.remove_child(expr)
        return True
    else:
        return False
