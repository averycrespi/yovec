from typing import Tuple

from engine.env import Env
from engine.node import Node
from engine.yovec.vector import BaseVector


def transpile(program: Node) -> Node:
    """Transpile a Yovec program to YOLOL."""
    env = Env(overwrite=False)
    children = []
    for line in program.children:
        child = line.children[0]
        if child.kind == 'import':
            env = _transpile_import(env, child)
        elif child.kind == 'export':
            _transpile_export(env, child)
        elif child.kind == 'let':
            env, out_line = _transpile_let(env, child)
            children.append(out_line)
    return Node(kind='program', children=children)


def _transpile_import(env: Env, import_: Node) -> Env:
    """Transpile an import statement."""
    assert import_.kind == 'import'
    ident = import_.children[0].children[0].value
    return env.update(ident, True)


def _transpile_export(env: Env, export: Node):
    """Transpile an export statement."""
    assert export.kind == 'export'
    ident = import_.children[0].children[0].value
    _ = env[ident]


def _transpile_let(env: Env, let: Node) -> Tuple[Env, Node]:
    """Transpile a let statement to a line."""
    assert let.kind == 'let'
    ident = let.children[0].children[0].value
    env, vector = _transpile_vexpr(env, let.children[1])
    simple = SimpleVector(vector)
    env = env.update(ident, simple)
    line = Node(kind='line', children=simple.assign())
    return env, line


def _transpile_vexpr(env: Env, vexpr: Node) -> Tuple[Env, Node]:
    """Transpile a vexpr to a vector."""
    if vexpr.kind == 'premap':
        #TODO
    elif vexpr.kind == 'postmap':
        #TODO
    elif vexpr.kind == 'concat':
        #TODO
    elif vexpr.kind == 'vecunary':
        #TODO
    elif vexpr.kind == 'vecbinary':
        #TODO
    elif vexpr.kind == 'variable':
        #TODO
    elif vexpr.kind == 'vector':
        #TODO
