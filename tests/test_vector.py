# pyre-ignore-all-errors
from hypothesis import given
from hypothesis.strategies import integers, lists
import pytest

from engine.errors import YovecError
from engine.transpile.number import Number
from engine.transpile.vector import Vector


@given(lns=lists(integers()), rns=lists(integers()))
def test_vecbinary(lns, rns):
    if len(lns) == 0 or len(rns) == 0:
        return
    left = Vector([Number(n) for n in lns])
    right = Vector([Number(n) for n in rns])
    if left.length != right.length:
        with pytest.raises(YovecError):
            vec = left.vecbinary('vec_add', right)
    else:
        vec = left.vecbinary('vec_add', right)
        assert vec.length == left.length == right.length


@given(ns=lists(integers()))
def test_map(ns):
    if len(ns) == 0:
        return
    vec = Vector([Number(n) for n in ns])
    res = vec.map('neg')
    assert res.length == vec.length


@given(ns=lists(integers()), m=integers())
def test_premap(ns, m):
    if len(ns) == 0:
        return
    vec = Vector([Number(n) for n in ns])
    num = Number(m)
    res = vec.premap('add', num)
    assert res.length == vec.length


@given(ns=lists(integers()), m=integers())
def test_postmap(ns, m):
    if len(ns) == 0:
        return
    vec = Vector([Number(n) for n in ns])
    num = Number(m)
    res = vec.postmap(num, 'add')
    assert res.length == vec.length


@given(lns=lists(integers()), rns=lists(integers()))
def test_apply(lns, rns):
    if len(lns) == 0 or len(rns) == 0:
        return
    left = Vector([Number(n) for n in lns])
    right = Vector([Number(n) for n in rns])
    if left.length != right.length:
        with pytest.raises(YovecError):
            vec = left.apply('add', right)
    else:
        vec = left.apply('add', right)
        assert vec.length == left.length == right.length


@given(lns=lists(integers()), rns=lists(integers()))
def test_concat(lns, rns):
    if len(lns) == 0 or len(rns) == 0:
        return
    left = Vector([Number(n) for n in lns])
    right = Vector([Number(n) for n in rns])
    vec = left.concat(right)
    assert vec.length == left.length + right.length


@given(ns=lists(integers()))
def test_reverse(ns):
    if len(ns) == 0:
        return
    vec = Vector([Number(n) for n in ns])
    res = vec.reverse()
    assert res.length == vec.length
