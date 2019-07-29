from logging import getLogger
from typing import Tuple

from engine.log import LOGGER_NAME
logger = getLogger(LOGGER_NAME)

from engine.context import context
from engine.errors import YovecError
from engine.node import Node

from engine.optimize.decimal import Decimal


def reduce_expressions(program: Node) -> Node:
    """Reduce expressions in a YOLOL program."""
    assert program.kind == 'program'
    logger.debug('reducing expressions')
    clone = program.clone()
    while _propagate_constants(clone) or _fold_constants(clone):
        pass
    return clone


def _propagate_constants(program: Node) -> bool:
    """Propagate constants in a program.

    Returns True if a constant was propagated.
    """
    assert program.kind == 'program'
    variables = program.find(lambda node: node.kind == 'variable')
    for var in variables:
        replacement, delta = _propagate_var(program, var)
        if delta:
            var.parent.replace_child(var, replacement) # type: ignore
            return True
    return False


def _propagate_var(program: Node, var: Node) -> Tuple[Node, bool]:
    """Propagate constants in a variable.

    Returns True if a constant was propagated.
    """
    if var.parent.kind == 'assignment' and var.parent.children.index(var) == 0: #$ type: ignore
        # Found "A" in "let A = expr"
        return var, False
    assignments = program.find(lambda node: node.kind == 'assignment' and node.children[0].value == var.value)
    if len(assignments) == 0:
        # Found external variable; cannot propagate
        return var, False
    expr = assignments[0].children[1].clone()
    if expr.kind == 'variable':
        # Found assignment of single variable
        return expr, True
    elif len(expr.find(lambda node: node.kind == 'variable')) == 0:
        # Found assignment of constant expression
        return expr, True
    else:
        return var, False


def _fold_constants(program: Node) -> bool:
    """Fold constants in a program.

    Returns True if constants were folded.
    """
    assert program.kind == 'program'
    assignments = program.find(lambda node: node.kind == 'assignment')
    for asn in assignments:
        if _fold_assignment(asn):
            return True
    return False


@context(statement='assignment')
def _fold_assignment(assignment: Node) -> bool:
    """Fold constants in an assignment.

    Returns True if constants were folded."""
    assert assignment.kind == 'assignment'
    numbers = assignment.find(lambda node: node.kind == 'number')
    for num in numbers:
        expr = num.parent
        for transform in Transform().functions:
            replacement, delta = transform(expr)
            if delta:
                expr.parent.replace_child(expr, replacement) # type: ignore
                return True
    return False


class Transform:
    """Store constant folding transformations."""
    def __init__(self):
        self.functions = (
            Transform.add_zero,
            Transform.sub_zero,
            Transform.mul_zero, Transform.mul_one,
            Transform.div_one,
            Transform.exp_zero, Transform.exp_one,
            Transform.binary_op
        )

    @staticmethod
    def is_binary_expr(expr: Node) -> bool:
        return len(expr.children) == 2 and expr.kind != 'assignment'

    @staticmethod
    @context(expression='expr')
    def add_zero(expr: Node) -> Tuple[Node, bool]:
        """Reduce (0+n) and (n+0) to (n)."""
        if not Transform.is_binary_expr(expr):
            return expr, False
        elif expr.kind == 'add' and expr.children[0].value == 0:
            return expr.children[1], True
        elif expr.kind == 'add' and expr.children[1].value == 0:
            return expr.children[0], True
        else:
            return expr, False

    @staticmethod
    @context(expression='expr')
    def sub_zero(expr: Node) -> Tuple[Node, bool]:
        """Reduce (n-0) to (0)."""
        if not Transform.is_binary_expr(expr):
            return expr, False
        elif expr.kind == 'sub' and expr.children[1].value == 0:
            return expr.children[0], True
        else:
            return expr, False

    @staticmethod
    @context(expression='expr')
    def mul_zero(expr: Node) -> Tuple[Node, bool]:
        """Reduce (0*n) and (n*0) to (0)."""
        if not Transform.is_binary_expr(expr):
            return expr, False
        elif expr.kind == 'mul' and expr.children[0].value == 0:
            return Node(kind='number', value='0'), True
        elif expr.kind == 'mul' and expr.children[1].value == 0:
            return Node(kind='number', value='0'), True
        else:
            return expr, False

    @staticmethod
    @context(expression='expr')
    def mul_one(expr: Node) -> Tuple[Node, bool]:
        """Reduce (1*n) and (n*1) to (n)."""
        if not Transform.is_binary_expr(expr):
            return expr, False
        elif expr.kind == 'mul' and expr.children[0].value == 1:
            return expr.children[1], True
        elif expr.kind == 'mul' and expr.children[1].value == 1:
            return expr.children[0], True
        else:
            return expr, False

    @staticmethod
    @context(expression='expr')
    def div_one(expr: Node) -> Tuple[Node, bool]:
        """Reduce (n/1) to (n)."""
        if not Transform.is_binary_expr(expr):
            return expr, False
        elif expr.kind == 'div' and expr.children[1].value == 1:
            return expr.children[0], True
        else:
            return expr, False

    @staticmethod
    @context(expression='expr')
    def exp_zero(expr: Node) -> Tuple[Node, bool]:
        """Reduce (0^n) to (0) and (n^0) to (1) for (n!=0)."""
        if not Transform.is_binary_expr(expr):
            return expr, False
        elif expr.kind == 'exp' and expr.children[0].value == 0 and expr.children[1].value != 0:
            return Node(kind='number', value='0'), True
        elif expr.kind == 'exp' and expr.children[0].value != 0 and expr.children[1].value == 0:
            return Node(kind='number', value='1'), True
        else:
            return expr, False

    @staticmethod
    @context(expression='expr')
    def exp_one(expr: Node) -> Tuple[Node, bool]:
        """Reduce (1^n) to (1) and (n^1) to (n)."""
        if not Transform.is_binary_expr(expr):
            return expr, False
        elif expr.kind == 'exp' and expr.children[0].value == 1:
            return Node(kind='number', value='1'), True
        elif expr.kind == 'exp' and expr.children[1].value == 1:
            return expr.children[0], True
        else:
            return expr, False

    @staticmethod
    @context(expression='expr')
    def binary_op(expr: Node) -> Tuple[Node, bool]:
        """Reduce a binary operation."""
        if not Transform.is_binary_expr(expr):
            return expr, False
        elif expr.children[0].kind == 'number' and expr.children[1].kind == 'number':
            try:
                left = Decimal(expr.children[0].value)
                right = Decimal(expr.children[1].value)
                result = str(left.binary(expr.kind, right)) # type: ignore
                return Node(kind='number', value=result), True
            except ArithmeticError:
                raise YovecError('failed to fold constants in binary expression')
        else:
            return expr, False
