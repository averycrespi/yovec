from copy import deepcopy
from typing import Union, Dict, Tuple, List

from engine.errors import YovecError
from engine.node import Node

from engine.transpile.function import Function
from engine.transpile.matrix import Matrix
from engine.transpile.number import Number
from engine.transpile.vector import Vector


Value = Union[Number, Vector, Matrix]


class Env:
    """Represents a program environment."""
    def __init__(self):
        self._num_index = 0
        self._vec_index = 0
        self._mat_index = 0

        self._variables = {}
        self._functions = {}
        self._imports = {}
        self._exports = {}

    @property
    def variables(self) -> Dict[str, Tuple[Value, int]]:
        return dict(self._variables)

    @property
    def functions(self) -> Dict[str, Function]:
        return dict(self._functions)

    @property
    def imports(self) -> Dict[str, str]:
        return dict(self._imports)

    @property
    def exports(self) -> Dict[str, str]:
        return dict(self._exports)

    def var(self, ident: str) -> Tuple[Value, int]:
        "Get the value of a variable."
        try:
            return self.variables[ident]
        except KeyError:
            raise YovecError('undefined variable: {}'.format(ident))

    def let(self, ident: str, value: Value) -> Tuple['Env', List[Node]]:
        """Assign a value to a variable."""
        if ident in self.variables:
            raise YovecError('cannot redefine existing variable: {}'.format(ident))
        elif ident in self.functions:
            raise YovecError('conflict between function and variable: {}'.format(ident))
        if type(value) == Number:
            index = self._num_index
            self._num_index += 1
        elif type(value) == Vector:
            index = self._vec_index
            self._vec_index += 1
        elif type(value) == Matrix:
            index = self._mat_index
            self._mat_index += 1
        else:
            raise AssertionError('fallthrough: {}'.format(type(value)))
        assignments, value = value.assign(index)
        clone = deepcopy(self)
        clone._variables[ident] = (value, index)
        return clone, assignments

    def func(self, ident: str) -> Function:
        """Get a function."""
        try:
            return self.functions[ident]
        except KeyError:
            raise YovecError('undefined function: {}'.format(ident))

    def define(self, ident: str, func: Function) -> 'Env':
        """Define a function."""
        if ident in self.functions:
            raise YovecError('cannot redefine existing function: {}'.format(ident))
        elif ident in self.variables:
            raise YovecError('conflict between function and variable: {}'.format(ident))
        clone = deepcopy(self)
        clone._functions[ident] = func
        return clone

    def target(self, alias: str) -> str:
        """Get the target of an alias."""
        if alias in self.imports:
            return self.imports[alias]
        elif alias in self.exports:
            return self.exports[alias]
        else:
            raise YovecError('undefined alias: {}'.format(alias))

    def import_(self, alias: str, target: str) -> 'Env':
        """Import an alias to a target."""
        if alias in self.imports:
            raise YovecError('cannot redefine existing import: {}'.format(alias))
        elif target in self.imports.values() or target in self.exports.values():
            raise YovecError('conflicting import target: {}'.format(target))
        clone = deepcopy(self)
        clone._imports[alias] = target
        return clone

    def export(self, alias: str, target: str) -> 'Env':
        """Export an alias to a target."""
        if alias not in self.variables:
            raise YovecError('cannot export undefined variable: {}'.format(alias))
        elif alias in self.exports:
            raise YovecError('cannot redefine existing export: {}'.format(alias))
        elif target in self.exports.values() or target in self.imports or target in self.imports.values():
            raise YovecError('conflicting export target: {}'.format(target))
        clone = deepcopy(self)
        clone._exports[alias] = target
        return clone
