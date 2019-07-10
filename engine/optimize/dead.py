from typing import Dict, Sequence, Set, Optional

from engine.node import Node


def eliminate_dead_code(program: Node, keep: Sequence[str]) -> Node:
    """Eliminate dead code from a YOLOL program."""
    assert program.kind == 'program'
    graph = _graph_deps(program)
    alive = _find_alive(graph, keep)
    return _prune_empty(_remove_dead(program, alive))


def _graph_deps(program: Node) -> Dict[str, Set[str]]:
    """Graph variable dependencies."""
    assert program.kind == 'program'
    graph = {}
    assignments = program.find(lambda node: node.kind == 'assignment')
    for a in assignments:
        variable = a.children[0]
        expr = a.children[1]
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
    for a in assignments:
        if a.children[0].value not in alive:
            a.parent.remove_child(a)
    return clone


def _prune_empty(program: Node) -> Node:
    """Prune empty lines."""
    assert program.kind == 'program'
    clone = program.clone()
    lines = clone.find(lambda node: node.kind == 'line')
    for line in lines:
        if len(line.children) == 0:
            line.parent.remove_child(line)
    return clone
