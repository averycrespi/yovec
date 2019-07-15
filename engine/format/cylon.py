import json
from typing import Any

from engine.node import Node


OPERATORS = {
    'neg': '-',
    'not': 'not',
    'abs': 'abs',
    'sqrt': 'sqrt',
    'sin': 'sin',
    'cos': 'cos',
    'tan': 'tan',
    'arcsin': 'arcsin',
    'arccos': 'arccos',
    'arctan': 'arctan',
    'exp': '^',
    'mul': '*',
    'div': '/',
    'mod': '%',
    'add': '+',
    'sub': '-',
    'lt': '<',
    'le': '<=',
    'gt': '>',
    'ge': '>=',
    'eq': '==',
    'ne': '!=',
    'or': 'or',
    'and': 'and'
}


def yolol_to_cylon(program: Node) -> str:
    """Format a YOLOL program as Cylon JSON."""
    assert program.kind == 'program'
    root = {'version': '0.2.0', 'program': _format_program(program)}
    return json.dumps(root, indent=4)


def _format_program(program: Node) -> Any:
    """Format a program."""
    assert program.kind == 'program'
    return {'type': 'program', 'lines': [_format_line(line) for line in program.children]}


def _format_line(line: Node) -> Any:
    """Format a line."""
    assert line.kind == 'line'
    return {'type': 'line', 'code': [_format_assignment(asn) for asn in line.children]}


def _format_assignment(assignment: Node) -> Any:
    """Format an assignment."""
    assert assignment.kind == 'assignment'
    identifier = assignment.children[0].value
    operator = '='
    value = _format_expression(assignment.children[1])
    return {'type': 'statement::assignment', 'identifier': identifier, 'operator': operator, 'value': value}


def _format_expression(expr: Node) -> Any:
    """Format an expression."""
    if expr.children is None:
        return {'type': 'expression::value', 'value': _format_value(expr)}
    elif len(expr.children) == 1:
        operand = _format_expression(expr.children[0])
        return {'type': 'expression::unary_op', 'operator': OPERATORS[expr.kind], 'operand': operand} # type: ignore
    elif len(expr.children) == 2:
        left = _format_expression(expr.children[0])
        right = _format_expression(expr.children[1])
        return {'type': 'expression::binary_op', 'operator': OPERATORS[expr.kind], 'left': left, 'right': right} # type: ignore
    else:
        raise AssertionError('unknown expression: {}'.format(expr))


def _format_value(value: Node) -> Any:
    """Format a value."""
    if value.kind == 'variable':
        return {'type': 'value::identifier', 'name': value.value}
    elif value.kind == 'number':
        return {'type': 'value::number', 'num': str(value.value)}
    else:
        raise AssertionError('unknown value: {}'.format(value))
