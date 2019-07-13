from typing import Tuple, Optional, Set

from engine.env import Env
from engine.errors import YovecError
from engine.node import Node
from engine.transpile.matrix import Matrix
from engine.transpile.number import Number
from engine.transpile.vector import Vector


def resolve_aliases(env: Env, program: Node) -> Tuple[Env, Node]:
    """Resolve aliases to their targets in a YOLOL program."""
    assert program.kind == 'program'
    resolved_imports = set()
    resolved_exports = set()
    clone = program.clone()

    for alias, target in env.imports.items():
        variables = clone.find(lambda node: node.kind == 'variable' and node.value == alias)
        for var in variables:
            var.value = target
            resolved_imports.add(target)

    for alias, target in env.exports.items():
        _, index = env.var(alias)

        num_prefix = '{}{}'.format(Number.PREFIX, index)
        num_variables = clone.find(lambda node: node.kind == 'variable' and node.value.startswith(num_prefix))
        for var in num_variables:
            var.value = var.value.replace(num_prefix, target) # type: ignore
            resolved_exports.add(var.value)
        if len(num_variables) > 0:
            continue

        vec_prefix = '{}{}'.format(Vector.PREFIX, index)
        vec_variables = clone.find(lambda node: node.kind == 'variable' and node.value.startswith(vec_prefix))
        for var in vec_variables:
            var.value = var.value.replace(vec_prefix, target) # type: ignore
            resolved_exports.add(var.value)
        if len(vec_variables) > 0:
            continue

        mat_prefix = '{}{}'.format(Matrix.PREFIX, index)
        mat_variables = clone.find(lambda node: node.kind == 'variable' and node.value.startswith(mat_prefix))
        for var in mat_variables:
            var.value = var.value.replace(mat_prefix, target) # type: ignore
            resolved_exports.add(var.value)
        if len(mat_variables) > 0:
            continue

    env = env.resolve_imports(list(resolved_imports))
    env = env.resolve_exports(list(resolved_exports))
    return env, clone
