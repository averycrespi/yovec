from copy import deepcopy
from typing import Dict, Sequence, Set, Optional

from engine.node import Node


def eliminate_dead_code(program: Node, keep: Sequence[str]) -> Node:
    """Eliminate dead code from a YOLOL program."""
    assert program.kind == 'program'
    graph = _graph_deps(program)
    alive = _find_alive(graph, keep)
    eliminated = _remove_assignments(program, alive)
    pruned = _prune_nodes(eliminated)
    return pruned


def _graph_deps(program: Node) -> Dict[str, Set[str]]:
    """Graph variable dependencies."""
    assert program.kind == 'program'
    graph = {}
    for line in program.children:
        for multi in line.children:
            for assignment in multi.children:
                variable = assignment.children[0]
                expr = assignment.children[1]
                graph[variable.value] = _find_vars(expr)
    return graph


def _find_vars(node: Node, vars: Optional[Set[str]]=None) -> Set[str]:
    """Find unique variables."""
    if vars is None:
        vars = set()
    if node.kind == 'variable':
        return vars | {node.value}
    elif node.children is None:
        return vars
    else:
        for c in node.children:
            vars = _find_vars(c, vars)
        return vars


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
            # External value
            pass
    return alive


def _remove_assignments(node: Node, alive: Set[str]) -> Node:
    """Remove dead assignments."""
    if node.kind == 'multi':
        remaining = []
        for assignment in node.children:
            var = assignment.children[0].value
            if var in alive:
                remaining.append(deepcopy(assignment))
        return Node(kind=node.kind, children=remaining)
    elif node.children is None:
        return node
    else:
        clone = deepcopy(node)
        clone.children = [_remove_assignments(c, alive) for c in clone.children]
        return clone


def _prune_nodes(program: Node) -> Node:
    """Prune empty nodes."""
    assert program.kind == 'program'
    pruned = Node(kind=program.kind, children=[])
    for line in program.children:
        multis = [m for m in line.children if len(m.children) > 0]
        if len(multis) > 0:
            pruned.children.append(Node(kind='line', children=deepcopy(multis)))
    return pruned
