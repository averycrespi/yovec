
from lark import Lark # type: ignore

from engine.context import Context
from engine.errors import YovecError
from engine.grammar import YOVEC_EBNF
from engine.node import Node

from engine.format.cylon import yolol_to_cylon
from engine.format.text import yolol_to_text

from engine.optimize.elim import eliminate_dead_code
from engine.optimize.mangle import mangle_names
from engine.optimize.reduce import reduce_expressions

from engine.transpile.transpiler import Transpiler


def run_yovec(source: str, root: str, no_elim: bool, no_reduce: bool, no_mangle: bool, ast: bool, cylon: bool) -> str:
    """Run Yovec."""
    try:
        parser = Lark(YOVEC_EBNF, start='program') # type: ignore
        yovec = Node.from_tree(parser.parse(source))
    except Exception as e:
        raise YovecError('Parse error: {}'.format(str(e)))

    try:
        transpiler = Transpiler(parser, root) # type: ignore
        yolol, imported, exported = transpiler.program(yovec)
    except YovecError as e:
        raise YovecError('Transpilation error: {}\n\n{}'.format(str(e), Context.format()))

    try:
        if not no_reduce:
            yolol = reduce_expressions(yolol)
        if not no_elim:
            yolol = eliminate_dead_code(yolol, exported) # type: ignore
        if not no_mangle:
            yolol = mangle_names(yolol, imported, exported) # type: ignore
    except YovecError as e:
        raise YovecError('Optimization error: {}\n\n{}'.format(str(e), Context.format()))

    if ast:
        return yolol.pretty()
    elif cylon:
        return yolol_to_cylon(yolol)
    else:
        return yolol_to_text(yolol)
