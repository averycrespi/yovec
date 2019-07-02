from lark import Lark

from engine.node import Node
from engine.yovec.prune import prune
from engine.yovec.validate import validate


with open('grammar/yovec.ebnf') as f:
    grammar = f.read()
parser = Lark(grammar, start='program')

with open('sample/dist.yovec') as f:
    raw_program = f.read()
program = parser.parse(raw_program)
program = Node.from_tree(program)
program = prune(program)

print(program.pretty())
