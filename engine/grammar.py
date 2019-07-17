from collections import namedtuple


Operator = namedtuple('Op', ('symbol', 'precedence'))
OPERATORS = {
    'neg': Operator('-', 100),
    'not': Operator('not', 90),
    'abs': Operator('abs', 90),
    'sqrt': Operator('sqrt', 90),
    'sin': Operator('sin', 90),
    'cos': Operator('cos', 90),
    'tan': Operator('tan', 90),
    'arcsin': Operator('arcsin', 90),
    'arccos': Operator('arccos', 90),
    'arctan': Operator('arctan', 90),
    'exp': Operator('^', 80),
    'mul': Operator('*', 70),
    'div': Operator('/', 70),
    'mod': Operator('%', 70),
    'add': Operator('+', 60),
    'sub': Operator('-', 60),
    'lt': Operator('<', 50),
    'le': Operator('<=', 50),
    'gt': Operator('>', 50),
    'ge': Operator('>=', 50),
    'eq': Operator('==', 40),
    'ne': Operator('!=', 40),
    'or': Operator('or', 30),
    'and': Operator('and', 20)
}

NEXPRS = (
    'num_binary',
    'num_unary',
    'reduce',
    'dot',
    'len',
    'rows',
    'cols',
    'vec_elem',
    'mat_elem',
    'external',
    'variable',
    'number'
)

VEXPRS = (
    'vec_binary',
    'vec_map',
    'vec_premap',
    'vec_postmap',
    'vec_apply',
    'concat',
    'reverse',
    'mat_row',
    'mat_col',
    'variable',
    'vector'
)

MEXPRS = (
    'mat_binary',
    'mat_map',
    'mat_premap',
    'mat_postmap',
    'mat_apply',
    'transpose',
    'mat_mul',
    'variable',
    'matrix'
)
