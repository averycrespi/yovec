import pytest # type: ignore

from engine.node import Node


def test_relationships():
    child = Node()
    assert child.parent is None
    assert child.children is None
    parent = Node(children=[child])
    assert parent.children is not None
    assert child in parent.children


def test_append_remove_child():
    child = Node()
    parent = Node()
    parent.append_child(child)
    assert parent.children is not None
    assert child in parent.children
    parent.remove_child(child)
    assert parent.children is not None
    assert child not in parent.children
    assert child.parent is None


def test_find():
    child = Node(kind='foo')
    parent = Node(children=[child])
    foo = parent.find(lambda node: node.kind == 'foo')
    assert child in foo
    bar = parent.find(lambda node: node.kind == 'bar')
    assert child not in bar
