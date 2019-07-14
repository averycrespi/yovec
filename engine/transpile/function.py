from typing import List

from engine.errors import YovecError
from engine.node import Node


TYPES = {
    'type_num': 'number',
    'type_vec': 'vector',
    'type_mat': 'matrix'
}


class Function:
    """Represents a function."""
    def __init__(self, ident: str, params: List[Node], return_type: Node, body: Node):
        assert len(params) > 0

        param_idents = [p.children[1].children[0].value for p in params]
        if len(set(param_idents)) < len(param_idents):
            raise YovecError('duplicate function parameters')

        body_vars = body.find(lambda node: node.kind == 'variable')
        for var in body_vars:
            var_ident = var.children[0].value
            if var_ident not in param_idents:
                raise YovecError('undefined variable in function scope: {}'.format(var_ident))

        if len(body.find(lambda node: node.kind == 'function' and node.children[0].value == ident)) > 0:
            raise YovecError('cannot recurse into function')

        self.ident = ident
        self.params = params
        self.return_type = return_type
        self.body = body

    def call_nexpr(self, args: List[Node]) -> Node:
        """Call a function and expect a nexpr."""
        if self.return_type.kind != 'type_num':
            raise YovecError('function returns {}, but caller expected number'.format(TYPES[self.return_type.kind]))
        return self._call(args)

    def call_vexpr(self, args: List[Node]) -> Node:
        """Call a function and expect a vexpr."""
        if self.return_type.kind != 'type_vec':
            raise YovecError('function returns {}, but caller expected vector'.format(TYPES[self.return_type.kind]))
        return self._call(args)

    def call_mexpr(self, args: List[Node]) -> Node:
        """Call a function and expect a mexpr."""
        if self.return_type.kind != 'type_mat':
            raise YovecError('function returns {}, but caller expected matrix'.format(TYPES[self.return_type.kind]))
        return self._call(args)

    def _call(self, args: List[Node]) -> Node:
        """Call a function."""
        if len(args) != len(self.params):
            raise YovecError('expected {} function arguments, but got {}'.format(len(params), len(args)))
        clone = self.body.clone()
        clone_vars = clone.find(lambda node: node.kind == 'variable')
        param_idents = [p.children[1].children[0].value for p in self.params]
        for var in clone_vars:
            ident = var.children[0].value
            index = param_idents.index(ident)
            replacement = args[index]
            var.parent.append_child(replacement)
            var.parent.remove_child(var)
        return clone
