from typing import Sequence

from engine.errors import YovecError
from engine.grammar import NEXPRS, VEXPRS, MEXPRS
from engine.node import Node


class Function:
    """Represents a function."""
    def __init__(self, ident: str, params: Sequence[Node], return_type: str, body: Node):
        self.param_types = [p.children[0].value for p in params]
        self.param_idents = [p.children[1].value for p in params]
        self.return_type = return_type
        self.body = body

        if len(set(self.param_idents)) < len(self.param_idents):
            raise YovecError('duplicate parameters')

        variables = body.find(lambda node: node.kind == 'variable')
        for var in variables:
            if var.value not in self.param_idents:
                raise YovecError('undefined variable: {}'.format(var.value))

        calls = body.find(lambda node: node.kind == 'call')
        for call in calls:
            if call.children[0].value == ident:
                raise YovecError('recursion is not allowed')

    def call(self, args: Sequence[Node]) -> Node:
        """Call a function with arguments."""
        if len(args) != len(self.param_idents):
            raise YovecError('expected {} arguments, but got {}'.format(len(self.param_idents), len(args)))

        for i, arg in enumerate(args):
            type_ = self.param_types[i]
            if type_ == 'number' and arg.kind not in NEXPRS:
                raise YovecError('expected argument to be number expression, but got {}'.format(arg.kind))
            elif type_ == 'vector' and arg.kind not in VEXPRS:
                raise YovecError('expected argument to be vector expression, but got {}'.format(arg.kind))
            elif type_ == 'matrix' and arg.kind not in MEXPRS:
                raise YovecError('expected argument to be matrix expression, but got {}'.format(arg.kind))

        clone = self.body.clone()
        variables = clone.find(lambda node: node.kind == 'variable')
        for var in variables:
            index = self.param_idents.index(var.value)
            var.parent.replace_child(var, args[index])
        return clone
