from copy import deepcopy
from typing import Tuple, List, Optional

from engine.errors import YovecError
from engine.node import Node
from engine.transpile.env import Env


Exported = Tuple[str]


def resolve_aliases(env: Env, node: Node, exported: Optional[Exported]=None) -> Tuple[Node, Exported]:
    """Resolve aliases to their targets."""
    if exported is None:
        exported = tuple()
    if node.kind == 'variable':
        for alias, target in env.aliases.items():
            if node.value == alias:
                return Node(kind=node.kind, value=target), exported
            try:
                num_index, _ = env.num(alias)
                prefix = 'n{}'.format(num_index)
                if node.value.startswith(prefix):
                    ident = node.value.replace(prefix, target)
                    return Node(kind=node.kind, value=ident), (*exported, ident)
            except YovecError:
                pass
            try:
                vec_index, _ = env.vec(alias)
                prefix = 'v{}e'.format(vec_index)
                if node.value.startswith(prefix):
                    ident = node.value.replace(prefix, target + '_')
                    return Node(kind=node.kind, value=ident), (*exported, ident)
            except YovecError:
                pass
            try:
                mat_index, _ = env.mat(alias)
                prefix = 'm{}'.format(mat_index)
                if node.value.startswith(prefix):
                    ident = node.value.replace(prefix, target + '_')
                    return Node(kind=node.kind, value=ident), (*exported, ident)
            except YovecError:
                pass
        return node, exported
    elif node.children is None:
        return node, exported
    else:
        clone = deepcopy(node)
        resolved = []
        for c in clone.children:
            r, e = resolve_aliases(env, c, exported)
            resolved.append(r)
            exported = e
        clone.children = resolved
        return clone, exported

