class YovecError(Exception):
    """Represents a general Yovec error."""
    pass


class Context:
    """Represents an error context."""
    statement = None
    local = None

    @classmethod
    def format(cls):
        output = ''
        if cls.statement is not None:
            output += 'In statement:\n\n{}\n'.format(cls.statement.pretty())
        if cls.local is not None:
            output += 'With node:\n\n{}\n'.format(cls.local.pretty())
        return output

