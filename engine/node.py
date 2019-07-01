SEP = '  '


class Node:
    """Represents an AST node."""
    def __init__(self, kind=None, value=None, children=None):
        self.kind = kind
        self.value = value
        self.children = children

    def __str__(self):
        if self.children is None:
            return '{} {}'.format(self.kind, self.value)
        p = ' '.join('({})'.format(str(c)) for c in self.children)
        return '{} {}'.format(self.kind, p)

    def _pretty(self, indent):
        if self.children is None:
            return '{}{} {}\n'.format(SEP * indent, self.kind, self.value)
        p = ''.join(c._pretty(indent+1) for c in self.children)
        return '{}{}\n{}'.format(SEP * indent, self.kind, p)

    def pretty(self):
        """Pretty-format a node."""
        return self._pretty(0)

    @staticmethod
    def from_tree(tree):
        """Make a node from a Lark parse tree."""
        if not hasattr(tree, 'data'):
            return Node(kind=tree.type, value=tree.value)
        node = Node(kind=tree.data, children=[Node.from_tree(c) for c in tree.children])
        return node
