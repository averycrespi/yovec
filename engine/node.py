from typing import List, Optional

from lark.tree import Tree


class Node:
    """Represents a generic AST node."""
    sep = '  '

    def __init__(self,
            kind: Optional[str]=None,
            value: Optional[str]=None,
            children: Optional[List['Node']]=None):
        self.kind = kind
        self.value = value
        self.children = children

    def __str__(self) -> str:
        if self.children is None:
            return '{} {}'.format(self.kind, self.value)
        p = ' '.join('({})'.format(str(c)) for c in self.children)
        return '{} {}'.format(self.kind, p)

    def _pretty(self, indent: int) -> str:
        if self.children is None:
            return '{}{} {}\n'.format(Node.sep * indent, self.kind, self.value)
        p = ''.join(c._pretty(indent+1) for c in self.children)
        return '{}{}\n{}'.format(Node.sep * indent, self.kind, p)

    def pretty(self) -> str:
        """Pretty-format a node."""
        return self._pretty(0)

    @staticmethod
    def from_tree(tree: Tree) -> 'Node':
        """Make a node from a Lark parse tree."""
        if not hasattr(tree, 'data'):
            return Node(kind=tree.type, value=tree.value)
        node = Node(kind=tree.data, children=[Node.from_tree(c) for c in tree.children])
        return node
