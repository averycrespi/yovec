from copy import deepcopy
from typing import Tuple, List

from engine.env import Env, NumVar, VecVar, MatVar
from engine.errors import YovecError
from engine.matrix import Matrix
from engine.node import Node
from engine.number import Number
from engine.vector import Vector


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
        elif child.kind == 'mat_let':
            env, mat_index, yolol_line = _transpile_mat_let(env, mat_index, child)
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
                    return Node(kind=node.kind, value=node.value.replace(prefix, target + '_'))
            except YovecError:
                pass
            try:
                mat_index, _ = env.var(alias, expect=MatVar)
                prefix = 'm{}'.format(mat_index)
                if node.value.startswith(prefix):
                    return Node(kind=node.kind, value=node.value.replace(prefix, target + '_'))
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
    env, num = _transpile_nexpr(env, let.children[1])
    assignment, num = num.assign(num_index)
    env = env.set_num(ident, num_index, num)
    multi = Node(kind='multi', children=[assignment])
    line = Node(kind='line', children=[multi])
    return env, num_index+1, line


def _transpile_vec_let(env: Env, vec_index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a vector let statement to a line."""
    assert let.kind == 'vec_let'
    ident = let.children[0].children[0].value
    env, vec = _transpile_vexpr(env, let.children[1])
    assignments, vec = vec.assign(vec_index)
    env = env.set_vec(ident, vec_index, vec)
    multi = Node(kind='multi', children=assignments)
    line = Node(kind='line', children=[multi])
    return env, vec_index+1, line


def _transpile_mat_let(env: Env, mat_index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a matrix let statement to a line."""
    assert let.kind == 'mat_let'
    ident = let.children[0].children[0].value
    env, mat = _transpile_mexpr(env, let.children[1])
    assignments, mat = mat.assign(mat_index)
    env = env.set_mat(ident, mat_index, mat)
    multi = Node(kind='multi', children=assignments)
    line = Node(kind='line', children=[multi])
    return env, mat_index+1, line


def _transpile_nexpr(env: Env, nexpr: Node) -> Tuple[Env, Number]:
    """Transpile a nexpr to a number."""
    if nexpr.kind == 'num_unary':
        env, num = _transpile_nexpr(env, nexpr.children[-1])
        for op in reversed(nexpr.children[:-1]):
            num = num.unary(op.kind)
        return env, num

    elif nexpr.kind == 'num_binary':
        env, lnum = _transpile_nexpr(env, nexpr.children[0])
        ops = nexpr.children[1::2]
        rnums = nexpr.children[2::2]
        for op, rnum in zip(ops, rnums):
            env, rnum = _transpile_nexpr(env, rnum)
            lnum = lnum.binary(op.kind, rnum)
        return env, lnum

    elif nexpr.kind == 'reduce':
        op = nexpr.children[0]
        env, vec = _transpile_vexpr(env, nexpr.children[1])
        return env, vec.reduce(op.kind)

    elif nexpr.kind == 'dot':
        env, lvec = _transpile_vexpr(env, nexpr.children[0])
        env, rvec = _transpile_vexpr(env, nexpr.children[1])
        return env, lvec.dot(rvec)

    elif nexpr.kind == 'len':
        env, vec = _transpile_vexpr(env, nexpr.children[0])
        return env, vec.len()

    elif nexpr.kind == 'rows':
        env, mat = _transpile_mexpr(env, nexpr.children[0])
        return env, mat.rows()

    elif nexpr.kind == 'cols':
        env, mat = _transpile_mexpr(env, nexpr.children[0])
        return env, mat.cols()

    elif nexpr.kind == 'external':
        ident = nexpr.children[0].value
        _ = env.alias(ident)
        return env, Number(ident)

    elif nexpr.kind == 'variable':
        ident = nexpr.children[0].value
        _. num = env.var(ident, expect=NumVar)
        return env, num

    elif nexpr.kind == 'number':
        try:
            return env, Number(int(nexpr.children[0].value))
        except ValueError:
            return env, Number(float(nexpr.children[0].value))

    else:
        raise AssertionError('unknown kind for nexpr: {}'.format(vexpr.kind))


def _transpile_vexpr(env: Env, vexpr: Node) -> Tuple[Env, Vector]:
    """Transpile a vexpr to a vector."""
    if vexpr.kind == 'vec_map':
        op = vexpr.children[0]
        env, vec = _transpile_vexpr(env, vexpr.children[1])
        return env, vec.map(op.kind)

    elif vexpr.kind == 'vec_premap':
        op = vexpr.children[0]
        env, num = _transpile_nexpr(env, vexpr.children[1])
        env, vec = _transpile_vexpr(env, vexpr.children[2])
        return env, vec.premap(op.kind, num)

    elif vexpr.kind == 'vec_postmap':
        env, num = _transpile_nexpr(env, vexpr.children[0])
        op = vexpr.children[1]
        env, vec = _transpile_vexpr(env, vexpr.children[2])
        return env, vec.postmap(num, op.kind)

    elif vexpr.kind == 'vec_apply':
        op = vexpr.children[0]
        env, lvec = _transpile_vexpr(env, vexpr.children[1])
        env, rvec = _transpile_vexpr(env, vexpr.children[2])
        return env, lvec.apply(op.kind, rvec)

    elif vexpr.kind == 'concat':
        env, lvec = _transpile_vexpr(env, vexpr.children[0])
        for rvec in vexpr.children[1:]:
            env, rvec = _transpile_vexpr(env, rvec)
            lvec = lvec.concat(rvec)
        return env, lvec

    elif vexpr.kind == 'vec_binary':
        env, lvec = _transpile_vexpr(env, vexpr.children[0])
        ops = vexpr.children[1::2]
        rvecs = vexpr.children[2::2]
        for op, rvec in zip(ops, rvecs):
            env, rvec = _transpile_vexpr(env, rvec)
            lvec = lvec.vecbinary(op.kind, rvec)
        return env, lvec

    elif vexpr.kind == 'variable':
        ident = vexpr.children[0].value
        _, vec = env.var(ident, expect=VecVar)
        return env, vec

    elif vexpr.kind == 'vector':
        numums = []
        for nexpr in vexpr.children:
            env, num = _transpile_nexpr(env, nexpr)
            numums.append(num)
        return env, Vector(numums)

    else:
        raise AssertionError('unknown kind for vexpr: {}'.format(vexpr.kind))


def _transpile_mexpr(env: Env, mexpr: Node) -> Tuple[Env, Matrix]:
    """Transpile a mexpr to a matrix."""
    if mexpr.kind == 'mat_map':
        op = mexpr.children[0]
        env, mat = _transpile_mexpr(env, mexpr.children[1])
        return env, mat.map(op.kind)

    elif mexpr.kind == 'mat_premap':
        op = mexpr.children[0]
        env, num = _transpile_nexpr(env, mexpr.children[1])
        env, mat = _transpile_mexpr(env, mexpr.children[2])
        return env, mat.premap(op.kind, num)

    elif mexpr.kind == 'mat_postmap':
        env, num = _transpile_nexpr(env, mexpr.children[0])
        op = mexpr.children[1]
        env, mat = _transpile_mexpr(env, mexpr.children[2])
        return env, mat.postmap(num, op.kind)

    elif mexpr.kind == 'mat_apply':
        op = mexpr.children[0]
        env, lmat = _transpile_mexpr(env, mexpr.children[1])
        env, rmat = _transpile_mexpr(env, mexpr.children[2])
        return env, lmat.apply(op.kind, rmat)

    elif mexpr.kind == 'transpose':
        env, mat = _transpile_mexpr(env, mexpr.children[0])
        return env, mat.transpose()

    elif mexpr.kind == 'mat_mul':
        env, lmat = _transpile_mexpr(env, mexpr.children[0])
        for rmat in mexpr.children[1:]:
            env, rmat = _transpile_mexpr(env, rmat)
            lmat = lmat.matmul(rmat)
        return env, lmat

    elif mexpr.kind == 'mat_binary':
        env, lmat = _transpile_mexpr(env, mexpr.children[0])
        ops = mexpr.children[1::2]
        rmats = mexpr.children[2::2]
        for op, rmat in zip(ops, rmats):
            env, rmat = _transpile_mexpr(env, rmat)
            lmat = lmat.matbinary(op.kind, rmat)
        return env, lmat

    elif mexpr.kind == 'variable':
        ident = mexpr.children[0].value
        _, mat = env.var(ident, expect=MatVar)
        return env, mat

    elif mexpr.kind == 'matrix':
        vececs = []
        for vexpr in mexpr.children:
            env, vec = _transpile_vexpr(env, vexpr)
            vececs.append(vec)
        return env, Matrix(vececs)

    else:
        raise AssertionError('unknown kind for mexpr: {}'.format(vexpr.kind))
