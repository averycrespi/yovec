from typing import Tuple

from engine.env import Env
from engine.node import Node
from engine.yovec.vector import SimpleVector
from engine.yovec.number import SimpleNumber


def transpile(program: Node) -> Node:
    """Transpile a Yovec program to YOLOL."""
    env = Env(overwrite=False)
    index = 0
    children = []
    for line in program.children:
        child = line.children[0]
        if child.kind == 'import':
            env = _transpile_import(env, child)
        elif child.kind == 'export':
            _transpile_export(env, child)
        elif child.kind == 'let':
            env, index, out_line = _transpile_let(env, index, child)
            children.append(out_line)
        else:
            raise ValueError('unknown kind for child of line: {}'.format(child.kind))
    return Node(kind='program', children=children)


def _transpile_import(env: Env, import_: Node) -> Env:
    """Transpile an import statement."""
    assert import_.kind == 'import'
    ident = import_.children[0].children[0].value
    return env.update(ident, True)


def _transpile_export(env: Env, export: Node):
    """Transpile an export statement."""
    assert export.kind == 'export'
    ident = export.children[0].children[0].value
    _ = env[ident]


def _transpile_let(env: Env, index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a let statement to a line."""
    assert let.kind == 'let'
    ident = let.children[0].children[0].value
    env, sv = _transpile_vexpr(env, let.children[1])
    env = env.update(ident, (index, sv))
    multi = Node(kind='multi', children=sv.assign(index))
    line = Node(kind='line', children=[multi])
    return env, index+1, line


def _transpile_vexpr(env: Env, vexpr: Node) -> Tuple[Env, SimpleVector]:
    """Transpile a vexpr to a simple vector."""
    if vexpr.kind == 'premap':
        op = vexpr.children[0].kind
        env, sn = _transpile_nexpr(env, vexpr.children[1])
        env, sv = _transpile_vexpr(env, vexpr.children[2])
        return env, sv.premap(op, sn)
    elif vexpr.kind == 'postmap':
        env, sn = _transpile_nexpr(env, vexpr.children[0])
        op = vexpr.children[1].kind
        env, sv = _transpile_vexpr(env, vexpr.children[2])
        return env, sv.postmap(sn, op)
    elif vexpr.kind == 'vecunary':
        op = vexpr.children[0].kind
        env, sv = _transpile_vexpr(env, vexpr.children[1])
        return env, sv.vecunary(op)
    elif vexpr.kind == 'vecbinary':
        env, lsv = _transpile_vexpr(env, vexpr.children[0])
        op = vexpr.children[1].kind
        env, rsv = _transpile_vexpr(env, vexpr.children[2])
        return env, lsv.vecbinary(op, rsv)
    elif vexpr.kind == 'variable':
        ident = vexpr.children[0].value
        _, sv = env[ident]
        return env, sv
    elif vexpr.kind == 'vector':
        snums = []
        for nexpr in vexpr.children:
            env, sn = _transpile_nexpr(env, nexpr)
            snums.append(sn)
        return env, SimpleVector(snums)
    else:
        raise ValueError('unknown kind for vexpr: {}'.format(vexpr.kind))


def _transpile_nexpr(env: Env, nexpr: Node) -> Tuple[Env, SimpleNumber]:
    """Transpile a nexpr to a simple number."""
    if nexpr.kind == 'unary':
        op = nexpr.children[0].kind
        env, sn = _transpile_nexpr(env, nexpr.children[1])
        return env, sn.unary(op)
    elif nexpr.kind == 'binary':
        env, lsn = _transpile_nexpr(env, nexpr.children[0])
        op = nexpr.children[1].kind
        env, rsn = _transpile_nexpr(env, nexpr.children[2])
        return env, lsn.binary(op, rsn)
    elif nexpr.kind == 'reduce':
        op = nexpr.children[0].kind
        env, sv = _transpile_vexpr(env, nexpr.children[1])
        return env, sv.reduce(op)
    elif nexpr.kind == 'dot':
        env, lsv = _transpile_vexpr(env, nexpr.children[0])
        env, rsv = _transpile_vexpr(env, nexpr.children[1])
        return lsv.dot(rsv)
    elif nexpr.kind == 'len':
        env, sv = _transpile_vexpr(env, nexpr.children[0])
        return sv.len()
    elif nexpr.kind == 'external':
        return env, SimpleNumber(nexpr.children[0].value)
    elif nexpr.kind == 'number':
        try:
            return env, SimpleNumber(int(nexpr.children[0].value))
        except ValueError:
            return env, SimpleNumber(float(nexpr.children[0].value))
    else:
        raise ValueError('unknown kind for nexpr: {}'.format(vexpr.kind))
