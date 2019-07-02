from engine.env import Env
from engine.node import Node



def validate(program: Node):
    """Validate a Yovec program."""
    env = Env(overwrite=False)
    _validate_idents(env, program)


def _validate_idents(env: Env, node: Node) -> Env:
    """Validate identifiers."""
    if node.kind == 'import':
        ident = node.children[0].children[0].value
        return env.update(ident, True)
    elif node.kind.startswith('let'):
        ident = node.children[0].children[0].value
        env = env.update(ident, True)
        return _validate_idents(env, node.children[1])
    elif node.kind in ('variable', 'external'):
        ident = node.children[0].value
        try:
            _ = env[ident]
            return env
        except KeyError:
            raise KeyError('undefined identifier: {}'.format(ident))
    elif node.kind == 'export':
        return _validate_idents(env, node.children[0])
    elif node.children is None:
        return env
    else:
        for c in node.children:
            env = _validate_idents(env, c)
        return env
