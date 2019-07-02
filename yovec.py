from lark import Lark

from engine.node import Node
from engine.yovec.prune import prune


with open('grammar/yovec.ebnf') as f:
    grammar = f.read()
parser = Lark(grammar, start='program')

with open('example/dist.yovec') as f:
    raw_program = f.read()
program = parser.parse(raw_program)
program = Node.from_tree(program)
program = prune(program)

print(program.pretty())
