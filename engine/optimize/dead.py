from typing import Dict, Sequence, Set, Optional

from engine.node import Node


def eliminate_dead_code(program: Node, keep: Sequence[str]) -> Node:
    """Eliminate dead code from a YOLOL program."""
    assert program.kind == 'program'
    graph = _graph_deps(program)
    alive = _find_alive(graph, keep)
    return _remove_dead(program, alive)


def _graph_deps(program: Node) -> Dict[str, Set[str]]:
    """Graph variable dependencies."""
    assert program.kind == 'program'
    graph = {}
    assignments = program.find(lambda node: node.kind == 'assignment')
    for asn in assignments:
        variable = asn.children[0]
        expr = asn.children[1]
        unique = {v.value for v in expr.find(lambda node: node.kind == 'variable')}
        graph[variable.value] = unique
    return graph


def _find_alive(graph: Dict[str, Set[str]], keep: Sequence[str]) -> Set[str]:
    """Find living variables."""
    queue = list(keep)
    alive = set()
    while len(queue) > 0:
        var = queue.pop()
        if var in alive:
            continue
        alive.add(var)
        try:
            queue.extend(list(graph[var]))
        except KeyError:
            pass
    return alive


def _remove_dead(program: Node, alive: Set[str]) -> Node:
    """Remove dead assignments."""
    assert program.kind == 'program'
    clone = program.clone()
    assignments = clone.find(lambda node: node.kind == 'assignment')
    for asn in assignments:
        if asn.children[0].value not in alive:
            assert asn.parent is not None
            asn.parent.remove_child(asn) # type: ignore
    lines = clone.find(lambda node: node.kind == 'line')
    for line in lines:
        if len(line.children) == 0:
            assert line.parent is not None
            line.parent.remove_child(line) # type: ignore
    return clone
