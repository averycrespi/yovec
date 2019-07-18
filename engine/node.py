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

    def append_child(self, child: 'Node'):
        """Append a child to a node."""
        if self.children is None:
            self._children = []
        self._children.append(child)
        child.parent = self

    def remove_child(self, child: 'Node'):
        """Remove the child of a node."""
        self._children.remove(child)
        child.parent = None

    def replace_child(self, original: 'Node', replacement: 'Node'):
        """Replace the child of a node."""
        index = self.children.index(original)
        self._children[index] = replacement
        original.parent = None
        replacement.parent = self

    def __str__(self) -> str:
        if self.children is None:
            return '{} {}'.format(self.kind, self.value)
        s = ' '.join('({})'.format(str(c)) for c in self.children)
        return '{} {}'.format(self.kind, s)

    def pretty(self, indent=0) -> str:
        """Pretty-format a node."""
        if self.children is None:
            return '{}{} {}\n'.format(Node.sep * indent, self.kind, self.value)
        s = ''.join(c.pretty(indent=indent+1) for c in self.children)
        return '{}{}\n{}'.format(Node.sep * indent, self.kind, s)

    def clone(self) -> 'Node':
        """Clone a node."""
        return deepcopy(self)

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

    def pfind(self, predicate: Callable[['Node'], bool], found: Optional[List['Node']]=None) -> List['Node']:
        """Recursively find parents that satisfy a predicate."""
        if found is None:
            found = []
        if predicate(self):
            found.append(self)
        if self.parent is not None:
            self.parent.pfind(predicate, found) # type: ignore
        return found

    @staticmethod
    def from_tree(tree: Tree) -> 'Node': # type: ignore
        """Make a node from a Lark parse tree."""
        if not hasattr(tree, 'data'):
            raise AssertionError('naked token: {}'.format(tree))
        elif len(tree.children) == 1 and not hasattr(tree.children[0], 'data'):
            # Unwrap terminal
            return Node(kind=tree.data, value=tree.children[0].value)
        else:
            return Node(kind=tree.data, children=[Node.from_tree(c) for c in tree.children])
