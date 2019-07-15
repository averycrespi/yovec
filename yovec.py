from argparse import ArgumentParser
from pathlib import Path
from sys import stderr

from lark import Lark # type: ignore

from engine.errors import YovecError
from engine.format.cylon import yolol_to_cylon
from engine.format.text import yolol_to_text
from engine.node import Node
from engine.optimize.elim import eliminate_dead_code
from engine.optimize.mangle import mangle_names
from engine.optimize.reduce import reduce_expressions
from engine.transpile.yolol import yovec_to_yolol, Context


__version__ = 'v1.6.0'


parser = ArgumentParser(description='Transpile Yovec to YOLOL')
parser.add_argument('-i', action='store', dest='infile', default=None, help='Yovec source file')
parser.add_argument('-o', action='store', dest='outfile', default=None, help='YOLOL output file (stdout if unset)')
parser.add_argument('--ast', action='store_true', help='output AST (overrides --cylon)')
parser.add_argument('--cylon', action='store_true', help='output Cylon JSON')
parser.add_argument('--no-elim', action='store_true', help='disable dead code elimination')
parser.add_argument('--no-mangle', action='store_true', help='disable name mangling')
parser.add_argument('--no-reduce', action='store_true', help='disable expression reduction')
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
    with open(Path('grammar') / 'yovec.ebnf') as f:
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
    yolol, imported, exported = yovec_to_yolol(yovec)
except YovecError as e:
    stderr.write('Transpilation error: {}\n'.format(str(e)))
    stderr.write('\nContext:\n\n{}\n'.format(Context().node.pretty()))
    exit(1)

# Optimize

try:
    if not args.no_reduce:
        yolol = reduce_expressions(yolol)
    if not args.no_elim:
        yolol = eliminate_dead_code(yolol, exported)
    if not args.no_mangle:
        yolol = mangle_names(yolol, imported, exported)
except YovecError as e:
    stderr.write('Optimization error: {}\n'.format(str(e)))
    exit(1)

# Output

if args.ast:
    output = yolol.pretty()
elif args.cylon:
    output = yolol_to_cylon(yolol)
else:
    output = yolol_to_text(yolol)

if args.outfile is None:
    print(output)
    exit(0)
else:
    with open(args.outfile, mode='w') as f:
        f.write(output)
    exit(0)
