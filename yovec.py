from lark import Lark

from engine.node import Node
from engine.yolol.format import format
from engine.yovec.transpile import transpile


with open('grammar/yovec.ebnf') as f:
    grammar = f.read()
parser = Lark(grammar, start='program')

with open('sample/dist.yovec') as f:
    raw_program = f.read()
yovec_program = Node.from_tree(parser.parse(raw_program))
yolol_program = transpile(yovec_program)

print(format(yolol_program))
