from collections import namedtuple

from engine.node import Node


# Higher precedence is evaluated first
Op = namedtuple('Op', ('symbol', 'precedence'))

OPERATORS = {
    'neg': Op('-', 100),
    'abs': Op('abs ', 90),
    'sqrt': Op('sqrt ', 90),
    'sin': Op('sin ', 90),
    'cos': Op('cos ', 90),
    'tan': Op('tan ', 90),
    'arcsin': Op('arcsin ', 90),
    'arccos': Op('arccos ', 90),
    'arctan': Op('arctan ', 90),
    'exp': Op('^', 80),
    'mul': Op('*', 70),
    'div': Op('/', 70),
    'mod': Op('%', 70),
    'add': Op('+', 60),
    'sub': Op('-', 60),
    'lt': Op('<', 50),
    'le': Op('<=', 50),
    'gt': Op('>', 50),
    'ge': Op('>=', 50),
    'eq': Op('==', 40),
    'ne': Op('!=', 40)
}


def format_yolol(program: Node) -> str:
    """Format a YOLOL program to text."""
    assert program.kind == 'program'
    return '\n'.join(_format_line(c) for c in program.children)


def _format_line(line: Node) -> str:
    """Format a line."""
    assert line.kind == 'line'
    return _format_multi(line.children[0])


def _format_multi(multi: Node) -> str:
    """Format multiple statements."""
    assert multi.kind == 'multi'
    return ' '.join(_format_statement(c) for c in multi.children)


def _format_statement(statement: Node) -> str:
    """Format a statement."""
    return _format_assignment(statement)


def _format_assignment(assignment: Node) -> str:
    """Format an assignment."""
    assert assignment.kind == 'assignment'
    return '{}={}'.format(assignment.children[0].value, _format_expr(assignment.children[1]))


def _format_expr(expr: Node, parent_prec: int=0) -> str:
    """Format an expression."""
    if expr.children is None:
        return expr.value
    elif len(expr.children) == 1:
        sym, prec = OPERATORS[expr.kind]
        return '{lparen}{sym}{child}{rparen}'.format(
            lparen= '(' if parent_prec > prec else '',
            sym=sym,
            child=_format_expr(expr.children[0], prec),
            rparen= ')' if parent_prec > prec else '',
        )
    elif len(expr.children) == 2:
        sym, prec = OPERATORS[expr.kind]
        return '{lparen}{lchild}{sym}{rchild}{rparen}'.format(
            lparen= '(' if parent_prec > prec else '',
            lchild=_format_expr(expr.children[0], prec),
            sym=sym,
            rchild=_format_expr(expr.children[1], prec),
            rparen= ')' if parent_prec > prec else ''
        )
    else:
        raise AssertionError('unrecognized expr: {}'.format(expr))
