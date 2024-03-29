from logging import getLogger
from pathlib import Path
from typing import Tuple, Set, Optional

from engine.log import LOGGER_NAME
logger = getLogger(LOGGER_NAME)

from engine.context import context
from engine.env import Env
from engine.grammar import is_nexpr, is_vexpr, is_mexpr
from engine.errors import YovecError
from engine.node import Node

from engine.transpile.macro import Macro
from engine.transpile.library import use_library
from engine.transpile.matrix import Matrix
from engine.transpile.number import Number
from engine.transpile.resolve import resolve_aliases
from engine.transpile.vector import Vector


class Transpiler:
    """Transpile Yovec to YOLOL."""
    def __init__(self, parser, root: Path):
        logger.debug('creating transpiler with root - {}'.format(root))
        self.parser = parser
        self.root = root

    def program(self, program: Node, env: Optional[Env]=None) -> Tuple[Env, Node]:
        """Transpile a program to YOLOL."""
        assert program.kind == 'program'
        logger.debug('transpiling program')
        if env is None:
            env = Env()
        yolol = Node(kind='program')
        statements = [line.children[0] for line in program.children]
        for statement in statements:
            if statement.kind == 'import_group':
                env = self.import_group(env, statement)
            elif statement.kind == 'export':
                env = self.export(env, statement)
            elif statement.kind.startswith('let'): # type: ignore
                env, line = self.let(env, statement)
                yolol.append_child(line)
            elif statement.kind.startswith('def'): # type: ignore
                env = self.define(env, statement)
            elif statement.kind == 'using':
                env = self.using(env, statement)
            elif statement.kind == 'comment':
                pass
            else:
                raise AssertionError('unexpected statement kind: {}'.format(statement.kind))
        return env, yolol

    @context(statement='group')
    def import_group(self, env: Env, group: Node) -> Env:
        """Transpile an import group to YOLOL."""
        assert group.kind == 'import_group'
        logger.debug('transpiling import group - {}'.format(group))
        for import_ in group.children:
            env = self.import_(env, import_)
        return env

    @context(statement='import_')
    def import_(self, env: Env, import_: Node) -> Env:
        """Transpile an import statement to YOLOL."""
        assert import_.kind == 'import'
        logger.debug('transpiling import statement - {}'.format(import_))
        target = import_.children[0].value.lower()
        if len(import_.children) == 2:
            alias = import_.children[1].value.lower()
        else:
            alias = target
        return env.import_(alias, target)

    @context(statement='export')
    def export(self, env: Env, export: Node):
        """Transpile an export statement to YOLOL."""
        assert export.kind == 'export'
        logger.debug('transpiling export statement - {}'.format(export))
        alias = export.children[0].value
        if len(export.children) == 2:
            target = export.children[1].value.lower()
        else:
            target = alias.lower()
        return env.export(alias, target)

    @context(statement='let')
    def let(self, env: Env, let: Node) -> Tuple[Env, Node]:
        """Transpile a let statement to YOLOL."""
        assert let.kind.startswith('let') # type: ignore
        logger.debug('transpiling let statement - {}'.format(let))
        ident = let.children[0].value
        expr = let.children[1]
        if let.kind == 'let_num':
            env, value = self.nexpr(env, expr)
        elif let.kind == 'let_vec':
            env, value = self.vexpr(env, expr)
        elif let.kind == 'let_mat':
            env, value = self.mexpr(env, expr)
        else:
            raise AssertionError('unexpected let kind: {}'.format(let.kind))
        env, assignments = env.let(ident, value)
        line = Node(kind='line', children=assignments)
        return env, line

    @context(statement='definition')
    def define(self, env: Env, definition: Node) -> Env:
        """Transpile a macro definition to YOLOL."""
        assert definition.kind.startswith('def') # type: ignore
        logger.debug('transpiling macro definition - {}'.format(definition))
        ident = definition.children[0].value
        params = definition.children[1].children
        body = definition.children[2]
        if definition.kind == 'def_num':
            return_type = 'number'
        elif definition.kind == 'def_vec':
            return_type = 'vector'
        elif definition.kind == 'def_mat':
            return_type = 'matrix'
        else:
            raise AssertionError('unexpected definition kind: {}'.format(definition.kind))
        macro = Macro(ident, params, return_type, body)
        return env.define(ident, macro)

    @context(statement='using')
    def using(self, env: Env, using: Node) -> Env:
        """Transpile a using statement to YOLOL."""
        logger.debug('transpiling using statement - {}'.format(using))
        assert using.kind == 'using'
        ident = using.children[0].value
        definitions = use_library(ident, self.parser, self.root)
        for def_ in definitions:
            env = self.define(env, def_)
        return env

    @context(expression='nexpr')
    def nexpr(self, env: Env, nexpr: Node) -> Tuple[Env, Number]:
        """Transpile a number expression to YOLOL."""
        logger.debug('transpiling number expression - {}'.format(nexpr))

        if not is_nexpr(nexpr.kind):
            raise YovecError('expected number expression, but got {}'.format(nexpr.kind))

        elif nexpr.kind == 'num_binary':
            env, lnum = self.nexpr(env, nexpr.children[0])
            ops = nexpr.children[1::2]
            rnums = nexpr.children[2::2]
            for op, rnum in zip(ops, rnums):
                env, rnum = self.nexpr(env, rnum)
                lnum = lnum.binary(op.kind, rnum)
            return env, lnum

        elif nexpr.kind == 'num_unary':
            env, num = self.nexpr(env, nexpr.children[-1])
            for op in reversed(nexpr.children[:-1]):
                num = num.unary(op.kind)
            return env, num

        elif nexpr.kind == 'reduce':
            op = nexpr.children[0]
            env, vec = self.vexpr(env, nexpr.children[1])
            return env, vec.reduce(op.kind)

        elif nexpr.kind == 'dot':
            env, lvec = self.vexpr(env, nexpr.children[0])
            env, rvec = self.vexpr(env, nexpr.children[1])
            return env, lvec.dot(rvec)

        elif nexpr.kind == 'len':
            env, vec = self.vexpr(env, nexpr.children[0])
            return env, vec.len()

        elif nexpr.kind == 'rows':
            env, mat = self.mexpr(env, nexpr.children[0])
            return env, mat.rows()

        elif nexpr.kind == 'cols':
            env, mat = self.mexpr(env, nexpr.children[0])
            return env, mat.cols()

        elif nexpr.kind == 'vec_elem':
            env, vec = self.vexpr(env, nexpr.children[0])
            index = nexpr.children[1].value
            try:
                return env, vec.elem(int(index))
            except ValueError:
                raise YovecError('invalid element index: {}'.format(index))

        elif nexpr.kind == 'mat_elem':
            env, mat = self.mexpr(env, nexpr.children[0])
            row = nexpr.children[1].value
            col = nexpr.children[2].value
            try:
                return env, mat.elem(int(row), int(col))
            except ValueError:
                raise YovecError('invalid element indices: {}, {}'.format(row, col))

        elif nexpr.kind == 'external':
            ident = nexpr.value
            _ = env.target(ident)
            return env, Number(ident)

        elif nexpr.kind == 'variable':
            ident = nexpr.value
            value, _ = env.var(ident)
            if type(value) != Number:
                raise YovecError('expected variable {} to be number, but got {}'.format(ident, value.class_name))
            return env, value

        elif nexpr.kind == 'call':
            ident = nexpr.children[0].value
            macro = env.macro(ident)
            if macro.return_type != 'number':
                raise YovecError('expected macro to return number expression, but got {} expression'.format(macro.return_type))
            args = nexpr.children[1].children
            return self.nexpr(env, macro.call(args))

        elif nexpr.kind == 'number':
            try:
                return env, Number(int(nexpr.value))
            except ValueError:
                return env, Number(float(nexpr.value))

        else:
            raise AssertionError('nexpr fallthough: {}'.format(nexpr))

    @context(expression='vexpr')
    def vexpr(self, env: Env, vexpr: Node) -> Tuple[Env, Vector]:
        """Transpile a vector expression to YOLOL."""
        logger.debug('transpiling vector expression - {}'.format(vexpr))

        if not is_vexpr(vexpr.kind):
            raise YovecError('expected vector expression, but got {}'.format(vexpr.kind))

        elif vexpr.kind == 'vec_binary':
            env, lvec = self.vexpr(env, vexpr.children[0])
            ops = vexpr.children[1::2]
            rvecs = vexpr.children[2::2]
            for op, rvec in zip(ops, rvecs):
                env, rvec = self.vexpr(env, rvec)
                lvec = lvec.vecbinary(op.kind, rvec)
            return env, lvec

        elif vexpr.kind == 'vec_map':
            op = vexpr.children[0]
            env, vec = self.vexpr(env, vexpr.children[1])
            return env, vec.map(op.kind)

        elif vexpr.kind == 'vec_premap':
            op = vexpr.children[0]
            env, num = self.nexpr(env, vexpr.children[1])
            env, vec = self.vexpr(env, vexpr.children[2])
            return env, vec.premap(op.kind, num)

        elif vexpr.kind == 'vec_postmap':
            env, num = self.nexpr(env, vexpr.children[0])
            op = vexpr.children[1]
            env, vec = self.vexpr(env, vexpr.children[2])
            return env, vec.postmap(num, op.kind)

        elif vexpr.kind == 'vec_apply':
            op = vexpr.children[0]
            env, lvec = self.vexpr(env, vexpr.children[1])
            for rvec in vexpr.children[1:]:
                env, rvec = self.vexpr(env, rvec)
                lvec = lvec.apply(op.kind, rvec)
            return env, lvec

        elif vexpr.kind == 'concat':
            env, lvec = self.vexpr(env, vexpr.children[0])
            for rvec in vexpr.children[1:]:
                env, rvec = self.vexpr(env, rvec)
                lvec = lvec.concat(rvec)
            return env, lvec

        elif vexpr.kind == 'reverse':
            env, vec = self.vexpr(env, vexpr.children[0])
            return env, vec.reverse()

        elif vexpr.kind == 'mat_row':
            env, mat = self.mexpr(env, vexpr.children[0])
            row = vexpr.children[1].value
            try:
                return env, mat.row(int(row))
            except ValueError:
                raise YovecError('invald row index: {}'.format(row))

        elif vexpr.kind == 'mat_col':
            env, mat = self.mexpr(env, vexpr.children[0])
            col = vexpr.children[1].value
            try:
                return env, mat.col(int(col))
            except ValueError:
                raise YovecError('invald column index: {}'.format(col))

        elif vexpr.kind == 'variable':
            ident = vexpr.value
            var, _ = env.var(ident)
            if type(var) != Vector:
                raise YovecError('expected variable {} to be vector, but got {}'.format(ident, var.class_name))
            return env, var

        elif vexpr.kind == 'call':
            ident = vexpr.children[0].value
            macro = env.macro(ident)
            if macro.return_type != 'vector':
                raise YovecError('expected macro to return vector expression, but got {} expression'.format(macro.return_type))
            args = vexpr.children[1].children
            return self.vexpr(env, macro.call(args))

        elif vexpr.kind == 'vector':
            numums = []
            for nexpr in vexpr.children:
                env, num = self.nexpr(env, nexpr)
                numums.append(num)
            return env, Vector(numums)

        else:
            raise AssertionError('vexpr fallthough: {}'.format(vexpr))

    @context(expression='mexpr')
    def mexpr(self, env: Env, mexpr: Node) -> Tuple[Env, Matrix]:
        """Transpile a matrix expression to YOLOL."""
        logger.debug('transpiling matrix expression - {}'.format(mexpr))

        if not is_mexpr(mexpr.kind):
            raise YovecError('expected matrix expression, but got {}'.format(mexpr.kind))

        elif mexpr.kind == 'mat_binary':
            env, lmat = self.mexpr(env, mexpr.children[0])
            ops = mexpr.children[1::2]
            rmats = mexpr.children[2::2]
            for op, rmat in zip(ops, rmats):
                env, rmat = self.mexpr(env, rmat)
                lmat = lmat.matbinary(op.kind, rmat)
            return env, lmat

        elif mexpr.kind == 'mat_map':
            op = mexpr.children[0]
            env, mat = self.mexpr(env, mexpr.children[1])
            return env, mat.map(op.kind)

        elif mexpr.kind == 'mat_premap':
            op = mexpr.children[0]
            env, num = self.nexpr(env, mexpr.children[1])
            env, mat = self.mexpr(env, mexpr.children[2])
            return env, mat.premap(op.kind, num)

        elif mexpr.kind == 'mat_postmap':
            env, num = self.nexpr(env, mexpr.children[0])
            op = mexpr.children[1]
            env, mat = self.mexpr(env, mexpr.children[2])
            return env, mat.postmap(num, op.kind)

        elif mexpr.kind == 'mat_apply':
            op = mexpr.children[0]
            env, lmat = self.mexpr(env, mexpr.children[1])
            for rmat in mexpr.children[1:]:
                env, rmat = self.mexpr(env, rmat)
                lmat = lmat.apply(op.kind, rmat)
            return env, lmat

        elif mexpr.kind == 'transpose':
            env, mat = self.mexpr(env, mexpr.children[0])
            return env, mat.transpose()

        elif mexpr.kind == 'mat_mul':
            env, lmat = self.mexpr(env, mexpr.children[0])
            env, rmat = self.mexpr(env, mexpr.children[1])
            return env, lmat.matmul(rmat)

        elif mexpr.kind == 'variable':
            ident = mexpr.value
            var, _ = env.var(ident)
            if type(var) != Matrix:
                raise YovecError('expected variable {} to be matrix, but got {}'.format(ident, var.class_name))
            return env, var

        elif mexpr.kind == 'call':
            ident = mexpr.children[0].value
            macro= env.macro(ident)
            if macro.return_type != 'matrix':
                raise YovecError('expected macro to return matrix expression, but got {} expression'.format(macro.return_type))
            args = mexpr.children[1].children
            return self.mexpr(env, macro.call(args))

        elif mexpr.kind == 'matrix':
            vecs = []
            for vexpr in mexpr.children:
                env, vec = self.vexpr(env, vexpr)
                vecs.append(vec)
            return env, Matrix(vecs)

        else:
            raise AssertionError('mexpr fallthough: {}'.format(mexpr))
