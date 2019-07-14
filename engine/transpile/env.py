from copy import deepcopy
from typing import Union, Dict, Tuple

from engine.errors import YovecError
from engine.transpile.function import Function
from engine.transpile.matrix import Matrix
from engine.transpile.number import Number
from engine.transpile.vector import Vector


Variable = Union[Number, Vector, Matrix]


class Env:
    """Represents a program environment."""
    def __init__(self):
        self._variables = {}
        self._functions = {}
        self._imports = {}
        self._exports = {}

    @property
    def variables(self) -> Dict[str, Tuple[Variable, int]]:
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

    def var(self, ident: str) -> Tuple[Variable, int]:
        try:
            return self.variables[ident]
        except KeyError:
            raise YovecError('undefined variable: {}'.format(ident))

    def set_var(self, ident: str, var: Variable, index: int) -> 'Env':
        if ident in self.variables:
            raise YovecError('cannot redefine existing variable: {}'.format(ident))
        if ident in self.functions:
            raise YovecError('name conflict between variable and function: {}'.format(ident))
        clone = deepcopy(self)
        clone._variables[ident] = (var, index)
        return clone

    def func(self, ident: str) -> Function:
        try:
            return self.functions[ident]
        except KeyError:
            raise YovecError('undefined function: {}'.format(ident))

    def set_func(self, ident: str, func: Function) -> 'Env':
        if ident in self.functions:
            raise YovecError('cannot redefine existing function: {}'.format(ident))
        if ident in self.variables:
            raise YovecError('name conflict between variable and function: {}'.format(ident))
        clone = deepcopy(self)
        clone._functions[ident] = func
        return clone

    def import_(self, alias: str) -> str:
        try:
            return self._imports[alias]
        except KeyError:
            raise YovecError('undefined import: {}'.format(alias))

    def set_import(self, alias: str, target: str) -> 'Env':
        if alias in self.imports:
            raise YovecError('cannot redefine existing import: {}'.format(alias))
        if target in self.imports.values() or target in self.exports.values():
            raise YovecError('conflicting import target: {}'.format(target))
        clone = deepcopy(self)
        clone._imports[alias] = target
        return clone

    def export(self, alias: str) -> str:
        try:
            return self.exports[alias]
        except KeyError:
            raise YovecError('undefined export: {}'.format(alias))

    def set_export(self, alias: str, target: str) -> 'Env':
        if alias not in self.variables:
            raise YovecError('cannot export undefined variable: {}'.format(alias))
        if alias in self.exports:
            raise YovecError('cannot redefine existing export: {}'.format(alias))
        if target in self.exports.values() or target in self.imports or target in self.imports.values():
            raise YovecError('conflicting export target: {}'.format(target))
        clone = deepcopy(self)
        clone._exports[alias] = target
        return clone
