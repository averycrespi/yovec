from functools import wraps
from inspect import getfullargspec as spec
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


def context(stmt: Optional[str]=None, expr: Optional[str]=None):
    """Set the context of a function."""
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if stmt is not None:
                Context.stmt = args[spec(func).args.index(stmt)]
            if expr is not None:
                Context.expr = args[spec(func).args.index(expr)]
            return func(*args, **kwargs)
        return inner
    return outer
