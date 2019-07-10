from argparse import ArgumentParser
from sys import stderr

from lark import Lark # type: ignore

from engine.errors import YovecError
from engine.format.text import yolol_to_text
from engine.node import Node
from engine.optimize.dead import eliminate_dead_code
from engine.transpile.yolol import yovec_to_yolol, Context


__version__ = 'v1.3.0'


parser = ArgumentParser(description='Transpile Yovec to YOLOL')
parser.add_argument('-i', action='store', dest='infile', default=None, help='Yovec source file')
parser.add_argument('-o', action='store', dest='outfile', default=None, help='YOLOL output file (stdout if unset)')
parser.add_argument('--ast', action='store_true', help='output AST')
parser.add_argument('--no-dead', action='store_true', help='disable dead code elimination')
parser.add_argument('--version', action='store_true', help='print version info')
args = parser.parse_args()

# Input

if args.version:
    print(__version__)
    exit(0)

if args.infile is None:
    parser.print_help()
    exit(1)

try:
    with open(args.infile) as f:
        text = f.read()
except IOError as e:
    stderr.write('Input error: {}\n'.format(str(e)))
    exit(1)

try:
    with open('grammar/yovec.ebnf') as f:
        grammar = f.read()
except IOError as e:
    stderr.write('Input error: {}\n'.format(str(e)))
    exit(1)

# Transpilation

try:
    yovec = Node.from_tree(Lark(grammar, start='program').parse(text))
except Exception as e:
    stderr.write('Parse error: {}\n'.format(str(e)))
    exit(1)

try:
    yolol, exported = yovec_to_yolol(yovec)
except YovecError as e:
    stderr.write('Transpilation error: {}\n'.format(str(e)))
    stderr.write('\nContext:\n\n{}\n'.format(Context().node.pretty()))
    exit(1)

# Optimize

if not args.no_dead:
    yolol = eliminate_dead_code(yolol, exported)

# Output

if args.ast:
    output = yolol.pretty()
else:
    output = yolol_to_text(yolol)

if args.outfile is None:
    print(output)
    exit(0)
else:
    with open(args.outfile, mode='w') as f:
        f.write(output)
    exit(0)
