from pathlib import Path
from typing import Sequence

from engine.errors import YovecError
from engine.node import Node

from engine.parse.yovec import parse_yovec


class Root:
    """Store the root directory."""
    dir_ = None
    @classmethod
    def set(cls, dir_):
        cls.dir_ = dir_


def use_library(ident: str) -> Sequence[Node]:
    """Use definitions from a library."""
    matches = list(Path(Root.dir_).glob('**/{}.lib.yovec'.format(ident))) # type: ignore
    if len(matches) == 0:
        raise YovecError('library not found: {}'.format(ident))
    if len(matches) > 1:
        raise YovecError('ambiguous library: {}'.format(ident))
    lib = matches[0]

    try:
        with open(lib) as f:
            text = f.read()
    except IOError as e:
        raise YovecError('unable to load library: {}'.format(str(e)))

    program = parse_yovec(text)
    statements = []
    for line in program.children:
        statement = line.children[0]
        if statement.kind == 'comment':
            continue
        if not statement.kind.startswith('def_'):
            raise YovecError('invalid statement in library: {}'.format(statement.kind))
        statements.append(statement)
    return statements
