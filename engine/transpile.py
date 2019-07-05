from typing import Tuple, List

from engine.env import Env
from engine.errors import YovecError
from engine.node import Node
from engine.number import SimpleNumber
from engine.vector import SimpleVector


IMPORT_PREFIX = '.IMPORT='
EXPORT_PREFIX = '.EXPORT='


def transpile_yovec(program: Node) -> Node:
    """Transpile a Yovec program to YOLOL.

    The environment contains:
        variable: (num_index, SimpleNumber)
        variable: (vec_index, SimpleVector)
        variable: (mat_index, SimpleMatrix)
        import before: True
        export before: after
    """
    env = Env(overwrite=False)
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
    return Node(kind='program', children=yolol_lines)


def _transpile_import(env: Env, import_: Node) -> Env:
    """Transpile an import statement."""
    assert import_.kind == 'import'
    before = import_.children[0].children[0].value
    try:
        return env.update(IMPORT_PREFIX + before, True)
    except KeyError as e:
        raise YovecError('failed to import variable') from e


def _transpile_export(env: Env, export: Node):
    """Transpile an export statement."""
    assert export.kind == 'export'
    before = export.children[0].children[0].value
    after = export.children[1].children[0].value
    try:
        _ = env[before]
    except KeyError as e:
        raise YovecError('failed to export variable') from e
    try:
        env = env.update(EXPORT_PREFIX + before, after)
    except KeyError as e:
        raise YovecError('failed to export variable') from e
    return env


def _transpile_num_let(env: Env, num_index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a number let statement to a line."""
    assert let.kind == 'num_let'
    ident = let.children[0].children[0].value
    env, sn = _transpile_nexpr(env, let.children[1])
    assignment, sn = sn.assign(num_index)
    try:
        env = env.update(ident, (num_index, sn))
    except KeyError as e:
        raise YovecError('failed to assign number') from e
    multi = Node(kind='multi', children=[assignment])
    line = Node(kind='line', children=[multi])
    return env, num_index+1, line


def _transpile_vec_let(env: Env, vec_index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a vector let statement to a line."""
    assert let.kind == 'vec_let'
    ident = let.children[0].children[0].value
    env, sv = _transpile_vexpr(env, let.children[1])
    assignments, sv = sv.assign(vec_index)
    try:
        env = env.update(ident, (vec_index, sv))
    except KeyError as e:
        raise YovecError('failed to assign vector') from e
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
        before = nexpr.children[0].value
        try:
            _ = env[IMPORT_PREFIX + before]
            return env, SimpleNumber(before)
        except KeyError as e:
            raise YovecError('undefined external: {}'.format(before)) from e
    elif nexpr.kind == 'variable':
        ident = nexpr.children[0].value
        _, sn = env[ident]
        if type(sn) != SimpleNumber:
            raise YovecError('expected variable {} to be a number, but got a {}'.format(ident, type(sn)))
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
        _, sv = env[ident]
        if type(sv) != SimpleVector:
            raise YovecError('expected variable {} to be a vector, but got a {}'.format(ident, type(sv)))
        return env, sv
    elif vexpr.kind == 'vector':
        snums = []
        for nexpr in vexpr.children:
            env, sn = _transpile_nexpr(env, nexpr)
            snums.append(sn)
        return env, SimpleVector(snums)
    else:
        raise AssertionError('unknown kind for vexpr: {}'.format(vexpr.kind))
