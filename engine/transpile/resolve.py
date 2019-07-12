from typing import Tuple, List, Optional

from engine.errors import YovecError
from engine.node import Node
from engine.transpile.env import Env


def resolve_aliases(env: Env, program: Node) -> Tuple[Node, List[str], List[str]]:
    """Resolve aliases to their targets in a YOLOL program."""
    assert program.kind == 'program'
    imported = []
    exported = []
    clone = program.clone()
    variables = clone.find(lambda node: node.kind == 'variable')
    for v in variables:
        for alias, target in env.aliases.items():
            if v.value == alias:
                v.value = target
                imported.append(v.value)
                break
            try:
                _, index = env.vector(alias)
                prefix = 'v{}'.format(index)
                if v.value.startswith(prefix):
                    v.value = v.value.replace(prefix, target)
                    exported.append(v.value)
                    break
            except YovecError:
                pass
    imported = list(set(imported))
    exported = list(set(exported))
    return clone, imported, exported
