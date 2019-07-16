from typing import Tuple, Optional, Set

from engine.errors import YovecError
from engine.node import Node

from engine.transpile.env import Env
from engine.transpile.matrix import Matrix
from engine.transpile.number import Number
from engine.transpile.vector import Vector


def resolve_aliases(env: Env, program: Node) -> Tuple[Node, Set[str], Set[str]]:
    """Resolve aliases to their targets in a YOLOL program."""
    assert program.kind == 'program'
    imported = set()
    exported = set()
    clone = program.clone()

    for alias, target in env.imports.items():
        variables = clone.find(lambda node: node.kind == 'variable' and node.value == alias)
        for var in variables:
            var.value = target
            imported.add(target)

    for alias, target in env.exports.items():
        var, index = env.var(alias)

        if type(var) == Number:
            num_prefix = '{}{}'.format(Number.PREFIX, index)
            num_variables = clone.find(lambda node: node.kind == 'variable' and node.value.startswith(num_prefix))
            for var in num_variables:
                var.value = var.value.replace(num_prefix, target) # type: ignore
                exported.add(var.value)

        elif type(var) == Vector:
            vec_prefix = '{}{}'.format(Vector.PREFIX, index)
            vec_variables = clone.find(lambda node: node.kind == 'variable' and node.value.startswith(vec_prefix))
            for var in vec_variables:
                var.value = var.value.replace(vec_prefix, target) # type: ignore
                exported.add(var.value)

        elif type(var) == Matrix:
            mat_prefix = '{}{}'.format(Matrix.PREFIX, index)
            mat_variables = clone.find(lambda node: node.kind == 'variable' and node.value.startswith(mat_prefix))
            for var in mat_variables:
                var.value = var.value.replace(mat_prefix, target) # type: ignore
                exported.add(var.value)

    return clone, imported, exported
