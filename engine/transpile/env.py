from collections import namedtuple
from copy import deepcopy
from string import ascii_uppercase
from typing import Union, Dict, Any

from engine.errors import YovecError
from engine.transpile.matrix import Matrix
from engine.transpile.number import Number
from engine.transpile.vector import Vector


NumVar = namedtuple('NumVar', ('index', 'number'))
VecVar = namedtuple('VecVar', ('index', 'vector'))
MatVar = namedtuple('MatVar', ('index', 'matrix'))


class Env:
    """Represents a program environment."""
    def __init__(self):
        self.variables = {}
        self.aliases = {}

    def vars(self) -> Dict[str, Union[NumVar, VecVar, MatVar]]:
        """Get all variables from the environment."""
        return dict(self.variables)

    def num(self, ident: str) -> NumVar:
        """Get a number variable."""
        try:
            n = self.variables[ident]
        except KeyError:
            raise YovecError('undefined variable: {}'.format(ident))
        if type(n) != NumVar:
            raise YovecError('expected variable {} to have type number, but got {}'.format(ident, n._fields[1]))
        return n

    def vec(self, ident: str) -> VecVar:
        """Get a vector variable."""
        try:
            v = self.variables[ident]
        except KeyError:
            raise YovecError('undefined variable: {}'.format(ident))
        if type(v) != VecVar:
            raise YovecError('expected variable {} to have type vector, but got {}'.format(ident, v._fields[1]))
        return v

    def mat(self, ident: str) -> MatVar:
        """Get a matrix variable."""
        try:
            m = self.variables[ident]
        except KeyError:
            raise YovecError('undefined variable: {}'.format(ident))
        if type(m) != MatVar:
            raise YovecError('expected variable {} to have type matrix, but got {}'.format(ident, m._fields[1]))
        return m

    def set_num(self, ident: str, index: int, num: Number) -> 'Env':
        """Set a number variable."""
        if ident in self.variables:
            raise YovecError('cannot redefine existing variable: {}'.format(ident))
        clone = deepcopy(self)
        clone.variables[ident] = NumVar(index=index, number=num)
        return clone

    def set_vec(self, ident: str, index: int, vec: Vector) -> 'Env':
        """Set a vector variable."""
        if ident in self.variables:
            raise YovecError('cannot redefine existing variable: {}'.format(ident))
        clone = deepcopy(self)
        clone.variables[ident] = VecVar(index=index, vector=vec)
        return clone

    def set_mat(self, ident: str, index: int, mat: Matrix) -> 'Env':
        """Set a matrix variable."""
        if ident in self.variables:
            raise YovecError('cannot redefine existing variable: {}'.format(ident))
        clone = deepcopy(self)
        clone.variables[ident] = MatVar(index=index, matrix=mat)
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
