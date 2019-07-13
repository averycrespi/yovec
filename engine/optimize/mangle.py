from itertools import product
from string import ascii_lowercase
from typing import Sequence

from engine.env import Env
from engine.node import Node


class Pool:
    """Generate names from a pool."""
    def __init__(self, excluded: Sequence[str]):
        self.excluded = excluded
        self.replaced = {}
        self.pool = []
        self.size = 1

    def gen(self) -> str:
        """Generate the next name."""
        if len(self.pool) == 0:
            self.pool = [''.join(x) for x in product(ascii_lowercase, repeat=self.size)]
            self.size += 1
        return self.pool.pop(0)

    def replace(self, name: str) -> str:
        """Replace a name."""
        if name in self.excluded:
            return name
        if name in self.replaced:
            return self.replaced[name]
        while True:
            replacement = self.gen()
            if replacement in self.excluded:
                continue
            self.replaced[name] = replacement
            return replacement


def mangle_names(env: Env, program: Node) -> Node:
    """Mangle names in a YOLOL program."""
    assert program.kind == 'program'
    clone = program.clone()
    pool = Pool([*env.resolved_imports, *env.resolved_exports])
    variables = clone.find(lambda node: node.kind == 'variable')
    for var in variables:
        var.value = pool.replace(var.value) # type: ignore
    return clone
