from lark import Lark


with open('grammar/yovec.ebnf') as f:
    grammar = f.read()
parser = Lark(grammar, start='program')

with open('example/dist.yovec') as f:
    raw_program = f.read()
program = parser.parse(raw_program)

print(program.pretty())
