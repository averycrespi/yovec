from functools import wraps
from inspect import getfullargspec as spec
from typing import Optional


class Context:
    """Stores the global context."""
    statement = None
    expression = None

    @classmethod
    def format(cls):
        return '{}{}'.format(
            'In statement:\n\n{}\n'.format(cls.statement.pretty()) if cls.statement is not None else '',
            'With expression:\n\n{}\n'.format(cls.expression.pretty()) if cls.expression is not None else ''
        )

def context(statement: Optional[str]=None, expression: Optional[str]=None):
    """Set the context of a function."""
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if statement is not None:
                Context.statement = args[spec(func).args.index(statement)]
                Context.expression = None
            if expression is not None:
                Context.expression = args[spec(func).args.index(expression)]
            return func(*args, **kwargs)
        return inner
    return outer
