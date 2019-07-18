from pathlib import Path

from lark import Lark # type: ignore

from engine.errors import YovecError
from engine.node import Node


GRAMMAR_FILE = Path('grammar') / 'yovec.ebnf'


def parse_yovec(text: str) -> Node:
    """Parse a Yovec program from text."""
    with open(GRAMMAR_FILE) as f:
        parser = Lark(f.read(), start='program') # type: ignore
    try:
        return Node.from_tree(parser.parse(text))
    except Exception as e:
        raise YovecError(str(e))
