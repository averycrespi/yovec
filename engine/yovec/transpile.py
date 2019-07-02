from typing import Tuple

from engine.env import Env
from engine.node import Node


def transpile(program: Node) -> Node:
    """Transpile a Yovec program to YOLOL."""
    env = Env(overwrite=False)
    children = []
    for line in program.children:
        env, out_line = _transpile_line(env, line)
        children.append(out_line)
    return Node(kind='program', children=children)


def _transpile_line(env: Env, line: Node) -> Tuple[Env, Node]:
    """Transpile a line."""
    pass #TODO: implement
