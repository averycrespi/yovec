# pyre-ignore-all-errors
from hypothesis import given
from hypothesis.strategies import integers
import pytest

from engine.transpile.number import Number


@given(n=integers())
def test_unary(n):
    num = Number(n).unary('neg')
    nexpr = num.evaluate()
    assert nexpr.kind == 'neg'
    assert len(nexpr.children) == 1
    assert nexpr.children[0].kind == 'number'
    assert nexpr.children[0].value == n


@given(n=integers(), m=integers())
def test_binary(n, m):
    num = Number(n).binary('add', Number(m))
    nexpr = num.evaluate()
    assert nexpr.kind == 'add'
    assert len(nexpr.children) == 2
    assert all(c.kind == 'number' for c in nexpr.children)


@given(n=integers())
def test_assign(n):
    assignment, num = Number(n).assign(0)
    assert assignment.kind == 'assignment'
    assert len(assignment.children) == 2
    assert assignment.children[0].kind == 'variable'
    assert assignment.children[0].value.startswith(Number.PREFIX)
