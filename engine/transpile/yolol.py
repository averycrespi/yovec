from typing import Tuple, Set

from engine.errors import YovecError
from engine.node import Node
from engine.transpile.env import Env
from engine.transpile.function import Function
from engine.transpile.matrix import Matrix
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


def yovec_to_yolol(program: Node) -> Tuple[Node, Set[str], Set[str]]:
    """Transpile a Yovec program to YOLOL."""
    Context().update(program)
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
        elif child.kind == 'define':
            env = _transpile_define(env, child)
        elif child.kind == 'comment':
            pass
        else:
            raise AssertionError('unknown kind for child: {}'.format(child.kind))
    yolol, imported, exported = resolve_aliases(env, Node(kind='program', children=yolol_lines))
    return yolol, imported, exported


def _transpile_import(env: Env, import_: Node) -> Env:
    """Transpile an import statement."""
    assert import_.kind == 'import'
    Context().update(import_)
    target = import_.children[0].children[0].value.lower()
    if len(import_.children) == 2:
        alias = import_.children[1].children[0].value.lower()
    else:
        alias = target
    return env.set_import(alias, target)


def _transpile_export(env: Env, export: Node):
    """Transpile an export statement."""
    assert export.kind == 'export'
    Context().update(export)
    alias = export.children[0].children[0].value
    target = export.children[1].children[0].value.lower()
    return env.set_export(alias, target)


def _transpile_num_let(env: Env, num_index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a number let statement to a line."""
    assert let.kind == 'num_let'
    Context().update(let)
    ident = let.children[0].children[0].value
    env, num = _transpile_nexpr(env, let.children[1])
    assignment, num = num.assign(num_index)
    env = env.set_var(ident, num, num_index)
    multi = Node(kind='multi', children=[assignment])
    line = Node(kind='line', children=[multi])
    return env, num_index+1, line


def _transpile_vec_let(env: Env, vec_index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a vector let statement to a line."""
    assert let.kind == 'vec_let'
    Context().update(let)
    ident = let.children[0].children[0].value
    env, vec = _transpile_vexpr(env, let.children[1])
    assignments, vec = vec.assign(vec_index)
    env = env.set_var(ident, vec, vec_index)
    multi = Node(kind='multi', children=assignments)
    line = Node(kind='line', children=[multi])
    return env, vec_index+1, line


def _transpile_mat_let(env: Env, mat_index: int, let: Node) -> Tuple[Env, int, Node]:
    """Transpile a matrix let statement to a line."""
    assert let.kind == 'mat_let'
    Context().update(let)
    ident = let.children[0].children[0].value
    env, mat = _transpile_mexpr(env, let.children[1])
    assignments, mat = mat.assign(mat_index)
    env = env.set_var(ident, mat, mat_index)
    multi = Node(kind='multi', children=assignments)
    line = Node(kind='line', children=[multi])
    return env, mat_index+1, line


def _transpile_define(env: Env, definition: Node) -> Env:
    """Transpile a define statement."""
    assert definition.kind == 'define'
    Context().update(definition)
    ident = definition.children[0].children[0].value
    params = definition.children[1:-2]
    return_type = definition.children[-2]
    body = definition.children[-1]
    func = Function(ident, params, return_type, body)
    env = env.set_func(ident, func)
    return env


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

    elif nexpr.kind == 'vec_elem':
        env, vec = _transpile_vexpr(env, nexpr.children[0])
        index = nexpr.children[1].children[0].value
        try:
            return env, vec.elem(int(index))
        except ValueError:
            raise YovecError('invalid element index: {}'.format(index))

    elif nexpr.kind == 'mat_elem':
        env, mat = _transpile_mexpr(env, nexpr.children[0])
        row = nexpr.children[1].children[0].value
        col = nexpr.children[2].children[0].value
        try:
            return env, mat.elem(int(row), int(col))
        except ValueError:
            raise YovecError('invalid element indices: {}, {}'.format(row, col))

    elif nexpr.kind == 'external':
        ident = nexpr.children[0].value
        _ = env.import_(ident)
        return env, Number(ident)

    elif nexpr.kind == 'call':
        ident = nexpr.children[0].children[0].value
        args = nexpr.children[1:]
        func = env.func(ident)
        return _transpile_nexpr(env, func.call_nexpr(args))

    elif nexpr.kind == 'variable':
        ident = nexpr.children[0].value
        var, _ = env.var(ident)
        if type(var) != Number:
            raise YovecError('expected variable {} to be number, but got {}'.format(ident, type(var)))
        return env, var

    elif nexpr.kind == 'number':
        try:
            return env, Number(int(nexpr.children[0].value))
        except ValueError:
            return env, Number(float(nexpr.children[0].value))

    else:
        raise AssertionError('unknown kind for nexpr: {}'.format(nexpr.kind))


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
        for rvec in vexpr.children[1:]:
            env, rvec = _transpile_vexpr(env, rvec)
            lvec = lvec.apply(op.kind, rvec)
        return env, lvec

    elif vexpr.kind == 'concat':
        env, lvec = _transpile_vexpr(env, vexpr.children[0])
        for rvec in vexpr.children[1:]:
            env, rvec = _transpile_vexpr(env, rvec)
            lvec = lvec.concat(rvec)
        return env, lvec

    elif vexpr.kind == 'reverse':
        env, vec = _transpile_vexpr(env, vexpr.children[0])
        return env, vec.reverse()

    elif vexpr.kind == 'mat_row':
        env, mat = _transpile_mexpr(env, vexpr.children[0])
        row = vexpr.children[1].children[0].value
        try:
            return env, mat.row(int(row))
        except ValueError:
            raise YovecError('invald row index: {}'.format(row))

    elif vexpr.kind == 'mat_col':
        env, mat = _transpile_mexpr(env, vexpr.children[0])
        col = vexpr.children[1].children[0].value
        try:
            return env, mat.col(int(col))
        except ValueError:
            raise YovecError('invald column index: {}'.format(col))

    elif vexpr.kind == 'vec_binary':
        env, lvec = _transpile_vexpr(env, vexpr.children[0])
        ops = vexpr.children[1::2]
        rvecs = vexpr.children[2::2]
        for op, rvec in zip(ops, rvecs):
            env, rvec = _transpile_vexpr(env, rvec)
            lvec = lvec.vecbinary(op.kind, rvec)
        return env, lvec

    elif vexpr.kind == 'call':
        ident = vexpr.children[0].children[0].value
        args = vexpr.children[1:]
        func = env.func(ident)
        return _transpile_vexpr(env, func.call_vexpr(args))

    elif vexpr.kind == 'variable':
        ident = vexpr.children[0].value
        var, _ = env.var(ident)
        if type(var) != Vector:
            raise YovecError('expected variable {} to be vector, but got {}'.format(ident, type(var)))
        return env, var

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
        for rmat in mexpr.children[1:]:
            env, rmat = _transpile_mexpr(env, rmat)
            lmat = lmat.apply(op.kind, rmat)
        return env, lmat

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

    elif mexpr.kind == 'call':
        ident = mexpr.children[0].children[0].value
        args = mexpr.children[1:]
        func = env.func(ident)
        return _transpile_mexpr(env, func.call_mexpr(args))

    elif mexpr.kind == 'variable':
        ident = mexpr.children[0].value
        var, _ = env.var(ident)
        if type(var) != Matrix:
            raise YovecError('expected variable {} to be matrix, but got {}'.format(ident, type(var)))
        return env, var

    elif mexpr.kind == 'matrix':
        vecs = []
        for vexpr in mexpr.children:
            env, vec = _transpile_vexpr(env, vexpr)
            vecs.append(vec)
        return env, Matrix(vecs)

    else:
        raise AssertionError('unknown kind for mexpr: {}'.format(mexpr.kind))
