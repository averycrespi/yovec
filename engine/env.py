from collections import namedtuple
from copy import deepcopy
from typing import Union, Dict, Any

from engine.errors import YovecError
from engine.number import SimpleNumber
from engine.vector import SimpleVector


NumVar = namedtuple('NumVar', ('index', 'sn'))
VecVar = namedtuple('VecVar', ('index', 'sv'))


class Env:
    """Represents a program environment."""
    def __init__(self):
        self.variables = {}
        self.aliases = {}

    def var(self, ident: str, expect: Any=None) -> Union[NumVar, VecVar]:
        """Get a variable from the environment."""
        try:
            v = self.variables[ident]
        except KeyError:
            raise YovecError('undefined variable: {}'.format(ident))
        if expect is not None and type(v) != expect:
            raise YovecError('expected variable to have type {}, but got {}'.format(expect, type(v)))
        return v

    def vars(self) -> Dict[str, Union[NumVar, VecVar]]:
        """Get all identifiers and variables from the environment."""
        return dict(self.variables)

    def set_num(self, ident: str, num_index: int, sn: SimpleNumber) -> 'Env':
        """Set a number variable."""
        if ident in self.variables:
            raise YovecError('cannot redefine existing variable: {}'.format(ident))
        clone = deepcopy(self)
        clone.variables[ident] = NumVar(index=num_index, sn=sn)
        return clone

    def set_vec(self, ident: str, vec_index: int, sv: SimpleVector) -> 'Env':
        """Set a vector variable."""
        if ident in self.variables:
            raise YovecError('cannot redefine existing variable: {}'.format(ident))
        clone = deepcopy(self)
        clone.variables[ident] = VecVar(index=vec_index, sv=sv)
        return clone

    def alias(self, ident: str) -> str:
        """Get an alias from the environment."""
        try:
            return self.aliases[ident]
        except KeyError:
            raise YovecError('undefined alias: {}'.format(ident))

    def aliases(self) -> Dict[str, str]:
        """Get all identifiers and aliases from the environment."""
        return dict(self.aliases)

    def set_alias(self, k: str, v: str) -> 'Env':
        """Set an alias."""
        if k in self.aliases:
            raise YovecError('cannot redefine existing alias: {}'.format(k))
        if v in self.aliases.values():
            raise YovecError('conflicting alias target: {}'.format(v))
        clone = deepcopy(self)
        clone.aliases[k] = v
        return clone
