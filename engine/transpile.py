from copy import deepcopy
from typing import Tuple, List

from engine.env import Env, NumVar, VecVar
from engine.errors import YovecError
from engine.node import Node
from engine.number import SimpleNumber
from engine.vector import SimpleVector


def transpile_yovec(program: Node) -> Node:
    """Transpile a Yovec program to YOLOL."""
    env = Env()
    num_index = 0
    vec_index = 0
    mat_index = 0
    yolol_lines = []
    for line in program.children:
        child = line.children[0]
        if child.kind == 'import':
            env = _transpile_import(env, child)
        elif child.kind == 'export':
            env = _transpile_export(env, child)
        elif child.kind == 'num_let':
            env, num_index, yolol_line = _transpile_num_let(env, num_index, child)
            yolol_lines.append(yolol_line)
        elif child.kind == 'vec_let':
            env, vec_index, yolol_line = _transpile_vec_let(env, vec_index, child)
            yolol_lines.append(yolol_line)
        elif child.kind == 'comment':
            pass
        else:
            raise AssertionError('unknown kind for child: {}'.format(child.kind))
    yolol_program = Node(kind='program', children=yolol_lines)
    return _resolve_aliases(env, yolol_program)


def _resolve_aliases(env: Env, node: Node) -> Node:
    """Resolve aliases to their targets."""
    if node.kind == 'variable':
        for alias, target in env.aliases.items():
            if node.value == alias:
                return Node(kind=node.kind, value=target)
            try:
                num_index, _ = env.var(alias, expect=NumVar)
                prefix = 'n{}'.format(num_index)
                if node.value.startswith(prefix):
                    return Node(kind=node.kind, value=node.value.replace(prefix, target))
            except YovecError:
                pass
            try:
                vec_index, _ = env.var(alias, expect=VecVar)
                prefix = 'v{}e'.format(vec_index)
                if node.value.startswith(prefix):
                    return Node(kind=node.kind, value=node.value.replace(prefix, target))
            except YovecError:
                pass
        return node
    elif node.children is None:
        return node
    else:
        clone = deepcopy(node)
        clone.children = [_resolve_aliases(env, c) for c in clone.children]
        return clone


def _transpile_import(env: Env, import_: Node) -> Env:
    """Transpile an import statement."""
    assert import_.kind == 'import'
    target = import_.children[0].children[0].value
    if len(import_.children) == 2:
        alias = import_.children[1].children[0].value
    else:
        alias = target
    return env.set_alias(alias, target)


def _transpile_export(env: Env, export: Node):
    """Transpile an export statement."""
    assert export.kind == 'export'
    alias = export.children[0].children[0].value
    target = export.children[1].children[0].value
    try:
        _ = env.var(alias)
    except YovecError as e:
        raise YovecError('cannot export undefined variable') from e
    return env.set_alias(alias, target)


def _transpile_num_let(env: Env, num_index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a number let statement to a line."""
    assert let.kind == 'num_let'
    ident = let.children[0].children[0].value
    env, sn = _transpile_nexpr(env, let.children[1])
    assignment, sn = sn.assign(num_index)
    env = env.set_num(ident, num_index, sn)
    multi = Node(kind='multi', children=[assignment])
    line = Node(kind='line', children=[multi])
    return env, num_index+1, line


def _transpile_vec_let(env: Env, vec_index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a vector let statement to a line."""
    assert let.kind == 'vec_let'
    ident = let.children[0].children[0].value
    env, sv = _transpile_vexpr(env, let.children[1])
    assignments, sv = sv.assign(vec_index)
    env = env.set_vec(ident, vec_index, sv)
    multi = Node(kind='multi', children=assignments)
    line = Node(kind='line', children=[multi])
    return env, vec_index+1, line


def _transpile_nexpr(env: Env, nexpr: Node) -> Tuple[Env, SimpleNumber]:
    """Transpile a nexpr to a simple number."""
    if nexpr.kind == 'num_unary':
        env, sn = _transpile_nexpr(env, nexpr.children[-1])
        for op in reversed(nexpr.children[:-1]):
            sn = sn.unary(op.kind)
        return env, sn

    elif nexpr.kind == 'num_binary':
        env, lsn = _transpile_nexpr(env, nexpr.children[0])
        ops = nexpr.children[1::2]
        rsns = nexpr.children[2::2]
        for op, rsn in zip(ops, rsns):
            env, rsn = _transpile_nexpr(env, rsn)
            lsn = lsn.binary(op.kind, rsn)
        return env, lsn

    elif nexpr.kind == 'reduce':
        op = nexpr.children[0]
        env, sv = _transpile_vexpr(env, nexpr.children[1])
        return env, sv.reduce(op.kind)

    elif nexpr.kind == 'dot':
        env, lsv = _transpile_vexpr(env, nexpr.children[0])
        env, rsv = _transpile_vexpr(env, nexpr.children[1])
        return env, lsv.dot(rsv)

    elif nexpr.kind == 'len':
        env, sv = _transpile_vexpr(env, nexpr.children[0])
        return env, sv.len()

    elif nexpr.kind == 'external':
        ident = nexpr.children[0].value
        _ = env.alias(ident)
        return env, SimpleNumber(ident)

    elif nexpr.kind == 'variable':
        ident = nexpr.children[0].value
        _. sn = env.var(ident, expect=NumVar)
        return env, sn

    elif nexpr.kind == 'number':
        try:
            return env, SimpleNumber(int(nexpr.children[0].value))
        except ValueError:
            return env, SimpleNumber(float(nexpr.children[0].value))

    else:
        raise AssertionError('unknown kind for nexpr: {}'.format(vexpr.kind))


def _transpile_vexpr(env: Env, vexpr: Node) -> Tuple[Env, SimpleVector]:
    """Transpile a vexpr to a simple vector."""
    if vexpr.kind == 'vec_map':
        op = vexpr.children[0]
        env, sv = _transpile_vexpr(env, vexpr.children[1])
        return env, sv.map(op.kind)

    elif vexpr.kind == 'vec_premap':
        op = vexpr.children[0]
        env, sn = _transpile_nexpr(env, vexpr.children[1])
        env, sv = _transpile_vexpr(env, vexpr.children[2])
        return env, sv.premap(op.kind, sn)

    elif vexpr.kind == 'vec_postmap':
        env, sn = _transpile_nexpr(env, vexpr.children[0])
        op = vexpr.children[1]
        env, sv = _transpile_vexpr(env, vexpr.children[2])
        return env, sv.postmap(sn, op.kind)

    elif vexpr.kind == 'concat':
        env, lsv = _transpile_vexpr(env, vexpr.children[0])
        for rsv in vexpr.children[1:]:
            env, rsv = _transpile_vexpr(env, rsv)
            lsv = lsv.concat(rsv)
        return env, lsv

    elif vexpr.kind == 'vec_binary':
        env, lsv = _transpile_vexpr(env, vexpr.children[0])
        ops = vexpr.children[1::2]
        rsvs = vexpr.children[2::2]
        for op, rsv in zip(ops, rsvs):
            env, rsv = _transpile_vexpr(env, rsv)
            lsv = lsv.vecbinary(op.kind, rsv)
        return env, lsv

    elif vexpr.kind == 'variable':
        ident = vexpr.children[0].value
        _, sv = env.var(ident, expect=VecVar)
        return env, sv

    elif vexpr.kind == 'vector':
        snums = []
        for nexpr in vexpr.children:
            env, sn = _transpile_nexpr(env, nexpr)
            snums.append(sn)
        return env, SimpleVector(snums)

    else:
        raise AssertionError('unknown kind for vexpr: {}'.format(vexpr.kind))
