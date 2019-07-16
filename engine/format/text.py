from collections import namedtuple
from sys import stderr

from engine.node import Node


Op = namedtuple('Op', ('symbol', 'precedence'))

NOOP = Op('', 0)
OPERATORS = {
    'neg': Op('-', 100),
    'not': Op(' not ', 90),
    'abs': Op(' abs ', 90),
    'sqrt': Op(' sqrt ', 90),
    'sin': Op(' sin ', 90),
    'cos': Op(' cos ', 90),
    'tan': Op(' tan ', 90),
    'arcsin': Op(' arcsin ', 90),
    'arccos': Op(' arccos ', 90),
    'arctan': Op(' arctan ', 90),
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
    'ne': Op('!=', 40),
    'or': Op(' or ', 30),
    'and': Op(' and ', 20)
}


def yolol_to_text(program: Node) -> str:
    """Format a YOLOL program as text."""
    assert program.kind == 'program'
    assignments = program.find(lambda node: node.kind == 'assignment')
    formatted = [_format_assignment(a) for a in assignments]
    text = ''
    curr = []
    for f in formatted:
        line = ' '.join(curr)
        if len(f) > 70:
            stderr.write('Warning: line exceeds 70 characters\n')
            text += '{}\n{}\n'.format(line, f)
            curr = []
        elif len(line) + len(' ') + len(f) > 70:
            text += '{}\n'.format(line)
            curr = [f]
        else:
            curr.append(f)
    if len(curr) > 0:
        text += '{}\n'.format(' '.join(curr))
    return text.strip('\n')


def _format_assignment(assignment: Node) -> str:
    """Format an assignment."""
    assert assignment.kind == 'assignment'
    variable = assignment.children[0].value
    expr = _format_expr(assignment.children[1], NOOP).strip()
    expr = expr.replace(' (', '(').replace('( ', '(')
    expr = expr.replace(' )', ')').replace(') ', ')')
    expr = expr.replace('  ', ' ')
    return '{}={}'.format(variable, expr)


def _format_expr(expr: Node, parent: Op) -> str:
    """Format an expression."""
    if expr.children is None:
        return str(expr.value)
    elif len(expr.children) == 1:
        op = OPERATORS[expr.kind] # type: ignore
        return '{lparen}{sym}{child}{rparen}'.format(
            lparen='(' if parent.precedence > op.precedence else '',
            sym=op.symbol,
            child=_format_expr(expr.children[0], op),
            rparen=')' if parent.precedence > op.precedence else '',
        )
    elif len(expr.children) == 2:
        op = OPERATORS[expr.kind] # type: ignore
        return '{lparen}{lchild}{sym}{rchild}{rparen}'.format(
            lparen='(' if parent.precedence > op.precedence else '',
            lchild=_format_expr(expr.children[0], op),
            sym=op.symbol,
            rchild=_format_expr(expr.children[1], op),
            rparen=')' if parent.precedence > op.precedence else ''
        )
    else:
        raise AssertionError('unexpected expression: {}'.format(expr))
