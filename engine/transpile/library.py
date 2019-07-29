from logging import getLogger
from pathlib import Path
from typing import Sequence

from engine.log import LOGGER_NAME
logger = getLogger(LOGGER_NAME)

from engine.errors import YovecError
from engine.node import Node


def use_library(ident: str, parser, root: str) -> Sequence[Node]:
    """Use definitions from a library."""
    logger.debug('using definitions from library - {}'.format(ident))
    matches = list(Path(root).glob('**/{}.lib.yovec'.format(ident))) # type: ignore
    if len(matches) == 0:
        raise YovecError('library not found: {}'.format(ident))
    if len(matches) > 1:
        raise YovecError('multiple files found for library {}: {}'.format(ident, [str(p) for p in matches]))

    try:
        with open(matches[0]) as f:
            text = f.read()
    except IOError as e:
        raise YovecError('unable to load library {}: {}'.format(ident, str(e)))

    try:
        program = Node.from_tree(parser.parse(text))
    except Exception as e:
        raise YovecError('failed to parse library {}: {}'.format(ident, str(e)))

    statements = [line.children[0] for line in program.children]
    definitions = []
    for statement in statements:
        if statement.kind == 'comment':
            continue
        elif statement.kind.startswith('def_'): # type: ignore
            definitions.append(statement)
        else:
            raise YovecError('invalid statement in library {}: {}'.format(ident, statement))
    return definitions
