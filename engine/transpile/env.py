from collections import namedtuple
from copy import deepcopy
from string import ascii_uppercase
from typing import Tuple, Dict

from engine.errors import YovecError
from engine.transpile.vector import Vector


class Env:
    """Represents a program environment."""
    def __init__(self):
        self.variables = {}
        self.aliases = {}

    def vector(self, ident: str) -> Tuple[Vector, int]:
        """Get a vector variable."""
        try:
            v, index = self.variables[ident]
        except KeyError:
            raise YovecError('undefined variable: {}'.format(ident))
        return v, index

    def set_vector(self, ident: str, v: Vector, index: int) -> 'Env':
        """Set a vector variable."""
        if ident in self.variables:
            raise YovecError('cannot redefine existing variable: {}'.format(ident))
        clone = deepcopy(self)
        clone.variables[ident] = (v, index)
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

    def set_alias(self, alias: str, target: str) -> 'Env':
        """Set an alias."""
        if alias in self.aliases:
            raise YovecError('cannot redefine existing alias: {}'.format(alias))
        if target in self.aliases.values():
            raise YovecError('conflicting alias target: {}'.format(target))
        if set(alias) in set(ascii_uppercase + '_') and alias not in self.variables:
            raise YovecError('cannot export undefined variable: {}'.format(alias))
        clone = deepcopy(self)
        clone.aliases[alias] = target
        return clone
