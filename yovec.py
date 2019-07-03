from argparse import ArgumentParser

from lark import Lark

from engine.node import Node
from engine.yolol.format import format
from engine.yovec.transpile import transpile


def parse_args():
    parser = ArgumentParser(description='Transpile Yovec to YOLOL')
    parser.add_argument('srcfile', type=str, help='Yovec source file')
    return parser.parse_args()


def main(srcfile):
    with open('grammar/yovec.ebnf') as f:
        grammar = f.read()
    parser = Lark(grammar, start='program')
    with open(srcfile) as f:
        raw_program = f.read()
    yovec_program = Node.from_tree(parser.parse(raw_program))
    yolol_program = transpile(yovec_program)
    print(format(yolol_program))


if __name__ == '__main__':
    args = parse_args()
    main(args.srcfile)
