from argparse import ArgumentParser

from lark import Lark

from engine.format import format_yolol
from engine.node import Node
from engine.transpile import transpile_yovec


def parse_args():
    parser = ArgumentParser(description='Transpile Yovec to YOLOL')
    parser.add_argument('srcfile', type=str, help='Yovec source file')
    parser.add_argument('--ast', action='store_true', help='Output YOLOL AST')
    return parser.parse_args()


def main(srcfile, ast=False):
    with open('grammar/yovec.ebnf') as f:
        grammar = f.read()
    parser = Lark(grammar, start='program')
    with open(srcfile) as f:
        raw_program = f.read()
    yovec_program = Node.from_tree(parser.parse(raw_program))
    yolol_program = transpile_yovec(yovec_program)
    if ast:
        print(yolol_program.pretty())
    else:
        print(format_yolol(yolol_program))


if __name__ == '__main__':
    args = parse_args()
    main(args.srcfile, ast=args.ast)
