from engine.node import Node
from engine.optimize.decimal import Decimal

from engine.context import context
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
        if var.parent.kind == 'assignment' and var.parent.children.index(var) == 0: # type: ignore
            # Ignore "A" in "let A = expr"
            continue
        if _propagate_var(program, var):
            return True
    return False


def _propagate_var(program: Node, var: Node):
    "Propagate constants in a variable."
    # Look for "let number var = expr"
    assignments = program.find(lambda node: node.kind == 'assignment' and node.children[0].value == var.value)
    if len(assignments) == 0:
        # Found external
        return False
    expr = assignments[0].children[1].clone()
    if expr.kind == 'variable':
        # Found "let A = B"
        var.parent.replace_child(var, expr)
        return True
    if len(expr.find(lambda node: node.kind == 'variable')) == 0:
        # Found "let A = 1 + 2 + 3"
        var.parent.replace_child(var, expr)
        return True
    return False


def _fold_constants(program: Node) -> bool:
    """Fold constants in a program."""
    assert program.kind == 'program'
    assignments = program.find(lambda node: node.kind == 'assignment')
    for asn in assignments:
        if _fold_assignment(asn):
            return True
    return False


@context(statement='assignment')
def _fold_assignment(assignment: Node) -> bool:
    """Fold constants in an assignment."""
    assert assignment.kind == 'assignment'
    numbers = assignment.find(lambda node: node.kind == 'number')
    for num in numbers:
        if num.parent == assignment: # type: ignore
            continue
        if len(num.parent.children) == 2 and _fold_binary_expr(num.parent): # type: ignore
            return True
    return False


@context(expression='expr')
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
    elif expr.kind == 'mul' and (left.value == 0 or right.value == 0):
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
            raise YovecError('failed to fold constants in binary expression')
    if delta:
        expr.parent.replace_child(expr, replacement)
        return True
    else:
        return False
