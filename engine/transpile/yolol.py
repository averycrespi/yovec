from typing import Tuple, List

from engine.errors import YovecError
from engine.node import Node
from engine.transpile.env import Env
from engine.transpile.number import Number
from engine.transpile.resolve import resolve_aliases
from engine.transpile.vector import Vector


class Context:
    """Store transpilation context."""
    _state = {}
    def __init__(self):
        self.__dict__ = self._state
    def update(self, node: Node):
        self.node = node


def yovec_to_yolol(program: Node) -> Tuple[Node, List[str], List[str]]:
    """Transpile a Yovec program to YOLOL."""
    Context().update(program)
    env = Env()
    index = 0
    yolol_lines = []
    for line in program.children:
        child = line.children[0]
        if child.kind == 'import':
            env = _transpile_import(env, child)
        elif child.kind == 'export':
            env = _transpile_export(env, child)
        elif child.kind == 'let':
            env, index, yolol_line = _transpile_let(env, index, child)
            yolol_lines.append(yolol_line)
        elif child.kind == 'comment':
            pass
        else:
            raise AssertionError('unknown kind for child: {}'.format(child.kind))
    return resolve_aliases(env, Node(kind='program', children=yolol_lines))


def _transpile_import(env: Env, import_: Node) -> Env:
    """Transpile an import statement."""
    assert import_.kind == 'import'
    Context().update(import_)
    target = import_.children[0].children[0].value
    if len(import_.children) == 2:
        alias = import_.children[1].children[0].value
    else:
        alias = target
    return env.set_alias(alias, target)


def _transpile_export(env: Env, export: Node):
    """Transpile an export statement."""
    assert export.kind == 'export'
    Context().update(export)
    alias = export.children[0].children[0].value
    target = export.children[1].children[0].value
    try:
        _ = env.vector(alias)
    except YovecError:
        raise YovecError('cannot export undefined variable: {}'.format(alias))
    return env.set_alias(alias, target)


def _transpile_let(env: Env, index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a let statement to a line."""
    assert let.kind == 'let'
    Context().update(let)
    ident = let.children[0].children[0].value
    env, vector = _transpile_vexpr(env, let.children[1])
    assignments, vector = vector.assign(prefix='v{}'.format(index))
    env = env.set_vector(ident, vector, index)
    multi = Node(kind='multi', children=assignments)
    line = Node(kind='line', children=[multi])
    return env, index+1, line


def _transpile_vexpr(env: Env, vexpr: Node) -> Tuple[Env, Vector]:
    """Transpile a vexpr to a vector."""
    Context().update(vexpr)
    if vexpr.kind == 'map_unary':
        op = vexpr.children[0]
        env, vector = _transpile_vexpr(env, vexpr.children[1])
        return env, vector.map_unary(op.kind)
    elif vexpr.kind == 'map_binary':
        op = vexpr.children[0].kind
        env, lv = _transpile_vexpr(env, vexpr.children[1])
        for e in vexpr.children[2:]:
            env, rv = _transpile_vexpr(env, e)
            lv = lv.map_binary(op, rv)
        return env, lv
    elif vexpr.kind == 'concat':
        env, lv = _transpile_vexpr(env, vexpr.children[0])
        for e in vexpr.children[1:]:
            env, rv = _transpile_vexpr(env, e)
            lv = lv.concat(rv)
        return env, lv
    elif vexpr.kind == 'dim':
        env, v = _transpile_vexpr(env, vexpr.children[0])
        return env, v.dim()
    elif vexpr.kind == 'dot':
        env, lv = _transpile_vexpr(env, vexpr.children[0])
        env, rv = _transpile_vexpr(env, vexpr.children[1])
        return env, lv.dot(rv)
    elif vexpr.kind == 'elem':
        env, v = _transpile_vexpr(env, vexpr.children[0])
        lit = vexpr.children[1].children[0].value
        return env, v.elem(lit)
    elif vexpr.kind == 'len':
        env, v = _transpile_vexpr(env, vexpr.children[0])
        return env, v.len()
    elif vexpr.kind == 'matmul':
        env, lv = _transpile_vexpr(env, vexpr.children[0])
        env, rv = _transpile_vexpr(env, vexpr.children[1])
        return env, lv.matmul(rv)
    elif vexpr.kind == 'reduce':
        op = vexpr.children[0]
        env, v = _transpile_vexpr(env, vexpr.children[1])
        return env, v.reduce(op.kind)
    elif vexpr.kind == 'repeat':
        env, v = _transpile_vexpr(env, vexpr.children[0])
        lit = vexpr.children[1].children[0].value
        return env, v.repeat(lit)
    elif vexpr.kind == 'reverse':
        env, v = _transpile_vexpr(env, vexpr.children[0])
        return env, v.reverse()
    elif vexpr.kind == 'transpose':
        env, v = _transpile_vexpr(env, vexpr.children[0])
        return env, v.transpose()
    elif vexpr.kind == 'literal':
        try:
            return env, Vector(Number(int(vexpr.children[0].value)))
        except ValueError:
            return env, Vector(Number(float(vexpr.children[0].value)))
    elif vexpr.kind == 'variable':
        ident = vexpr.children[0].value
        v, _ = env.vector(ident)
        return env, v
    elif vexpr.kind == 'external':
        ident = vexpr.children[0].value
        _ = env.alias(ident)
        return env, Vector(Number(ident))
    elif vexpr.kind == 'vector':
        vectors = []
        for e in vexpr.children:
            env, v = _transpile_vexpr(env, e)
            vectors.append(v)
        return env, Vector(vectors)
    else:
        raise AssertionError('unknown kind for vexpr: {}'.format(vexpr.kind))
