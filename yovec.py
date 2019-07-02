from lark import Lark

from engine.node import Node
from engine.yovec.dep import graph


with open('grammar/yovec.ebnf') as f:
    grammar = f.read()
parser = Lark(grammar, start='program')

with open('example/dist.yovec') as f:
    raw_program = f.read()
program = Node.from_tree(parser.parse(raw_program))

print(program.pretty())
print(graph(program))
