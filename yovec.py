from argparse import ArgumentParser
from sys import stderr

from lark import Lark

from engine.errors import YovecError
from engine.format.text import yolol_to_text
from engine.node import Node
from engine.transpile.yolol import yovec_to_yolol, Context


__version__ = 'v1.2'


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
    with open(infile) as f:
        text = f.read()
    yolol = transform(grammar, text)
    output = yolol.pretty() if ast else yolol_to_text(yolol)
    if outfile == '':
        print(output)
        exit(0)
    with open(outfile, mode='w') as f:
        f.write(output)
    exit(0)


def transform(grammar: str, text: str) -> Node:
    try:
        parser = Lark(grammar, start='program')
        yovec = Node.from_tree(parser.parse(text))
    except Exception as e:
        stderr.write('Parse error: {}\n'.format(str(e)))
        exit(1)
    try:
        yolol, exported = yovec_to_yolol(yovec)
        return yolol
    except YovecError as e:
        stderr.write('Transpilation error: {}\n'.format(str(e)))
        stderr.write('\nContext:\n\n{}\n'.format(Context().node.pretty()))
        exit(1)


if __name__ == '__main__':
    parser, args = parse_args()
    if args.version:
        print(__version__)
    elif args.i == '':
        parser.print_help(sys.stderr)
    else:
        main(args.i, args.o, ast=args.ast)
