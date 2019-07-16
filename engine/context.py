from functools import wraps
from typing import Optional


class Context:
    """Stores the global transpilation context."""
    stmt = None
    expr = None

    @classmethod
    def format(cls):
        s = ''
        if cls.stmt is not None:
            s += 'In statement:\n\n{}\n'.format(cls.stmt.pretty())
        if cls.expr is not None:
            s += 'With expression:\n\n{}\n'.format(cls.expr.pretty())
        return s


def context(stmt_index: Optional[int]=None, expr_index: Optional[int]=None):
    """Set the context of a function."""
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if stmt_index is not None:
                Context.stmt = args[stmt_index]
            if expr_index is not None:
                Context.expr = args[expr_index]
            return func(*args, **kwargs)
        return inner
    return outer
