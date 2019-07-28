from argparse import ArgumentParser, FileType
from os.path import realpath, dirname
from pathlib import Path
from sys import stdin, stdout, stderr, exit

from engine.errors import YovecError
from engine.run import run_yovec
from engine.version import VERSION


parser = ArgumentParser(description='Transpile Yovec to YOLOL')

parser.add_argument('-i', action='store', dest='infile', default=stdin,
        type=FileType('r'), help='Yovec source file (stdin if unset)')
parser.add_argument('-o', action='store', dest='outfile', default=stdout,
        type=FileType('w'), help='YOLOL output file (stdout if unset)')

parser.add_argument('--ast', action='store_true', help='output Yovec AST (overrides --cylon)')
parser.add_argument('--cylon', action='store_true', help='output Cylon JSON')
parser.add_argument('--no-elim', action='store_true', help='disable dead code elimination')
parser.add_argument('--no-mangle', action='store_true', help='disable name mangling')
parser.add_argument('--no-reduce', action='store_true', help='disable expression reduction')
parser.add_argument('--version', action='store_true', help='print version info')

args = parser.parse_args()

if args.version:
    print(VERSION)
    exit(0)

try:
    source = args.infile.read()
except IOError as e:
    stderr.write('Input error: {}\n'.format(str(e)))
    exit(1)

try:
    output = run_yovec(
        source,
        root=Path(dirname(realpath(__file__))),
        no_elim=args.no_elim,
        no_reduce=args.no_reduce,
        no_mangle=args.no_mangle,
        ast=args.ast,
        cylon=args.cylon
    )
except YovecError as e:
    stderr.write('{}\n'.format(str(e)))
    exit(1)
except Exception as e:
    stderr.write('Unexpected error: {}\n'.format(str(e)))
    exit(1)

try:
    args.outfile.write(output + '\n')
except IOError as e:
    stderr.write('Output error: {}\n'.format(str(e)))
    exit(1)

exit(0)
