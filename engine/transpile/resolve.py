from typing import Tuple, List, Optional

from engine.errors import YovecError
from engine.node import Node
from engine.transpile.env import Env


def resolve_aliases(env: Env, program: Node) -> Tuple[Node, List[str]]:
    """Resolve aliases to their targets in a YOLOL program."""
    assert program.kind == 'program'
    exported = []
    clone = program.clone()
    variables = clone.find(lambda node: node.kind == 'variable')
    for v in variables:
        for alias, target in env.aliases.items():
            if v.value == alias:
                v.value = target
                break
            try:
                num_index, _ = env.num(alias)
                prefix = 'n{}'.format(num_index)
                if v.value.startswith(prefix):
                    v.value = v.value.replace(prefix, target)
                    exported.append(v.value)
                    break
            except YovecError:
                pass
            try:
                vec_index, _ = env.vec(alias)
                prefix = 'v{}e'.format(vec_index)
                if v.value.startswith(prefix):
                    v.value = v.value.replace(prefix, target + '_')
                    exported.append(v.value)
                    break
            except YovecError:
                pass
            try:
                mat_index, _ = env.mat(alias)
                prefix = 'm{}'.format(mat_index)
                if v.value.startswith(prefix):
                    v.value = v.value.replace(prefix, target + '_')
                    exported.append(v.value)
                    break
            except YovecError:
                pass
    return clone, exported
