from copy import deepcopy
from typing import List, Optional, Callable

from lark.tree import Tree # type: ignore


class Node:
    """Represents a generic AST node."""
    sep = '  '

    def __init__(self, kind: Optional[str]=None, value: Optional[str]=None, children: Optional[List['Node']]=None):
        self.kind = kind
        self.value = value
        self._children = children
        self.parent = None
        if self._children is not None:
            for c in self.children:
                c.parent = self

    @property
    def children(self):
        return self._children

    def __str__(self) -> str:
        if self.children is None:
            return '{} {}'.format(self.kind, self.value)
        s = ' '.join('({})'.format(str(c)) for c in self.children)
        return '{} {}'.format(self.kind, s)

    def _pretty(self, indent: int) -> str:
        if self.children is None:
            return '{}{} {}\n'.format(Node.sep * indent, self.kind, self.value)
        s = ''.join(c._pretty(indent+1) for c in self.children)
        return '{}{}\n{}'.format(Node.sep * indent, self.kind, s)

    def pretty(self) -> str:
        """Pretty-format a node."""
        return self._pretty(0)

    def clone(self) -> 'Node':
        """Clone a node."""
        return deepcopy(self)

    def remove_child(self, child: 'Node'):
        """Remove the child of a node."""
        assert self._children is not None
        self._children.remove(child)

    def find(self, predicate: Callable[['Node'], bool], found: Optional[List['Node']]=None) -> List['Node']:
        """Recursively find children that satisfy a predicate."""
        if found is None:
            found = []
        if predicate(self):
            found.append(self)
        if self.children is not None:
            for c in self.children:
                c.find(predicate, found)
        return found

    @staticmethod
    def from_tree(tree: Tree) -> 'Node': # type: ignore
        """Make a node from a Lark parse tree."""
        if not hasattr(tree, 'data'):
            return Node(kind=tree.type, value=tree.value)
        return Node(kind=tree.data, children=[Node.from_tree(c) for c in tree.children])
