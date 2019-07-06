from argparse import ArgumentParser
import sys

from lark import Lark

from engine.format import format_yolol
from engine.node import Node
from engine.transpile import transpile_yovec


__version__ = 'v1.0'


def parse_args():
    parser = ArgumentParser(description='Transpile Yovec to YOLOL')
    parser.add_argument('-i', action='store', default='', help='Yovec source file')
    parser.add_argument('-o', action='store', default='', help='YOLOL output file (if unset, prints to stdout)')
    parser.add_argument('--ast', action='store_true', help='Output YOLOL AST')
    parser.add_argument('--version', action='store_true', help='Print version info')
    return parser, parser.parse_args()


def main(infile, outfile, ast=False):
    with open('grammar/yovec.ebnf') as f:
        grammar = f.read()
    parser = Lark(grammar, start='program')
    with open(infile) as f:
        raw_program = f.read()
    yovec_program = Node.from_tree(parser.parse(raw_program))
    yolol_program = transpile_yovec(yovec_program)
    if ast:
        output = yolol_program.pretty()
    else:
        output = format_yolol(yolol_program)
    if outfile == '':
        print(output)
    else:
        with open(outfile, mode='w') as f:
            f.write(output)


if __name__ == '__main__':
    parser, args = parse_args()
    if args.version:
        print(__version__)
    elif args.i == '':
        parser.print_help(sys.stderr)
    else:
        main(args.i, args.o, ast=args.ast)
