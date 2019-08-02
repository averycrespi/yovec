from collections import namedtuple


YOVEC_EBNF = r"""
%import common.WS
%ignore WS

// =========
// Terminals
// =========

COMMENT: /\/\/[^\n]*/
LITERAL: /-?\d+(\.\d{1,4})?/
VAR_IDENT: /[A-Z_]+/
MACRO_IDENT: /[a-zA-Z0-9_]+/
LIB_IDENT: /[a-zA-Z0-9_]+/
YOLOL_IDENT: /[a-zA-Z_][a-zA-Z0-9_]*/

// ==========
// Statements
// ==========

program: line*

line: import_group | export | let | define | using | comment

import_group: "import" (import ",")* import ("," import)*
import: external ("as" external)?

export: "export" variable ("as" external)?

?let: "let" "number" variable "=" nexpr     -> let_num
    | "let" "vector" variable "=" vexpr     -> let_vec
    | "let" "matrix" variable "=" mexpr     -> let_mat

?define: "define" macro param_group "->" "number" "=" nexpr     -> def_num
       | "define" macro param_group "->" "vector" "=" vexpr     -> def_vec
       | "define" macro param_group "->" "matrix" "=" mexpr     -> def_mat

using: "using" library
library: LIB_IDENT

comment: COMMENT

// =========
// Variables
// =========

variable: VAR_IDENT

external: YOLOL_IDENT

// ======
// Macros
// ======

macro: MACRO_IDENT

param_group: "(" (param ",")* param ("," param)* ")"
param: type variable

?type: "number"     -> type_num
     | "vector"     -> type_vec
     | "matrix"     -> type_mat

call: macro "!" args

args: "(" (expr ",")* expr ("," expr)* ")"

?expr: nexpr | vexpr | mexpr

// =======
// Numbers
// =======

number: LITERAL

?num_unary_op: "neg"        -> neg
             | "not"        -> not
             | "abs"        -> abs
             | "sqrt"       -> sqrt
             | "sin"        -> sin
             | "cos"        -> cos
             | "tan"        -> tan
             | "arcsin"     -> arcsin
             | "arccos"     -> arccos
             | "arctan"     -> arctan

?num_binary_op: "+"     -> add
              | "-"     -> sub
              | "*"     -> mul
              | "/"     -> div
              | "%"     -> mod
              | "^"     -> exp
              | "<"     -> lt
              | "<="    -> le
              | ">"     -> gt
              | ">="    -> ge
              | "=="    -> eq
              | "!="    -> ne
              | "and"   -> and
              | "or"    -> or

?nexpr: nbin

?nbin: nbase
     | nbin (num_binary_op nbase)+      -> num_binary

?nbase: (num_unary_op)+ nexpr           -> num_unary
      | "reduce" num_binary_op vexpr    -> reduce
      | vexpr "dot" vexpr               -> dot
      | "len" vexpr                     -> len
      | "rows" mexpr                    -> rows
      | "cols" mexpr                    -> cols
      | "elem" vexpr number             -> vec_elem
      | "elem" mexpr number number      -> mat_elem
      | "(" nexpr ")"
      | "$" external
      | variable
      | call
      | number

// =======
// Vectors
// =======

vector: "[" (nexpr ",")* nexpr ("," nexpr)* "]"

?vec_binary_op: "+"     -> vec_add
              | "-"     -> vec_sub

?vexpr: vbin

?vbin: vbase
      | vbin (vec_binary_op vbase)+         -> vec_binary

?vbase: "map" num_unary_op vexpr            -> vec_map
      | "map" num_binary_op nexpr vexpr     -> vec_premap
      | "map" nexpr num_binary_op vexpr     -> vec_postmap
      | "apply" num_binary_op vexpr+        -> vec_apply
      | "concat" vexpr+                     -> concat
      | "reverse" vexpr                     -> reverse
      | "row" mexpr number                  -> mat_row
      | "col" mexpr number                  -> mat_col
      | "(" vexpr ")"
      | variable
      | call
      | vector

// ========
// Matrices
// ========

matrix: "[" (vexpr ",")* vexpr ("," vexpr)* "]"

?mat_binary_op: "+"     -> mat_add
              | "-"     -> mat_sub

?mexpr: mbin

?mbin: mbase
     | mbin (mat_binary_op mbase)+          -> mat_binary

?mbase: "map" num_unary_op mexpr            -> mat_map
      | "map" num_binary_op nexpr mexpr     -> mat_premap
      | "map" nexpr num_binary_op mexpr     -> mat_postmap
      | "apply" num_binary_op mexpr+        -> mat_apply
      | "transpose" mexpr                   -> transpose
      | mexpr "@" mexpr                     -> mat_mul
      | "(" mexpr ")"
      | variable
      | call
      | matrix
"""


Operator = namedtuple('Op', ('symbol', 'precedence'))
OPERATORS = {
    'neg': Operator('-', 100),
    'not': Operator('not', 90),
    'abs': Operator('abs', 90),
    'sqrt': Operator('sqrt', 90),
    'sin': Operator('sin', 90),
    'cos': Operator('cos', 90),
    'tan': Operator('tan', 90),
    'arcsin': Operator('arcsin', 90),
    'arccos': Operator('arccos', 90),
    'arctan': Operator('arctan', 90),
    'exp': Operator('^', 80),
    'mul': Operator('*', 70),
    'div': Operator('/', 70),
    'mod': Operator('%', 70),
    'add': Operator('+', 60),
    'sub': Operator('-', 60),
    'lt': Operator('<', 50),
    'le': Operator('<=', 50),
    'gt': Operator('>', 50),
    'ge': Operator('>=', 50),
    'eq': Operator('==', 40),
    'ne': Operator('!=', 40),
    'or': Operator('or', 30),
    'and': Operator('and', 20)
}


_NEXPRS = (
    'num_binary',
    'num_unary',
    'reduce',
    'dot',
    'len',
    'rows',
    'cols',
    'vec_elem',
    'mat_elem',
    'external',
    'variable',
    'call',
    'number'
)


_VEXPRS = (
    'vec_binary',
    'vec_map',
    'vec_premap',
    'vec_postmap',
    'vec_apply',
    'concat',
    'reverse',
    'mat_row',
    'mat_col',
    'variable',
    'call',
    'vector'
)


_MEXPRS = (
    'mat_binary',
    'mat_map',
    'mat_premap',
    'mat_postmap',
    'mat_apply',
    'transpose',
    'mat_mul',
    'variable',
    'call',
    'matrix'
)


def is_nexpr(kind: str) -> bool:
    return kind in _NEXPRS


def is_vexpr(kind: str) -> bool:
    return kind in _VEXPRS


def is_mexpr(kind: str) -> bool:
    return kind in _MEXPRS
