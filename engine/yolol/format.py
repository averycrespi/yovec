from collections import namedtuple

from engine.node import Node


Op = namedtuple('Op', ('symbol', 'precedence'))

OPERATORS = {
    'neg': Op('-', 5),
    'add': Op('+', 1),
    'sub': Op('-', 1),
    'mul': Op('*', 2),
    'div': Op('/', 2),
    'mod': Op('%', 2),
    'exp': Op('^', 3),
    'abs': Op('abs ', 4),
    'sqrt': Op('sqrt ', 4),
    'sin': Op('sin ', 4),
    'cos': Op('cos ', 4),
    'tan': Op('tan ', 4),
    'arcsin': Op('arcsin ', 4),
    'arccos': Op('arccos ', 4),
    'arctan': Op('arctan ', 4)
}


def format(program: Node) -> str:
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
        raise ValueError('unrecognized expr: {}'.format(expr))
