from typing import Dict, Set

from engine.node import Node


def prune(program: Node) -> Node:
    """Prune unused dependencies from a Yovec program."""
    assert program.kind == 'program'
    graph = _graph_deps(program)
    used = _find_exported(program)
    before, after = 0, len(used)
    while before != after:
        before = len(used)
        for ident in used:
            try:
                used = used.union(graph[ident])
            except KeyError:
                raise KeyError('undefined dependency: {}'.format(ident))
        after = len(used)
    #TODO: remove unused
    return program


def _graph_deps(program: Node) -> Dict[str, Set[str]]:
    """Graph the dependencies of a program."""
    assert program.kind == 'program'
    graph = {}
    for line in program.children:
        child = line.children[0]
        if child.kind.startswith('let'):
            ident = child.children[0].children[0].value
            graph[ident] = _find_deps(child)
    return graph


def _find_deps(node: Node) -> Set[str]:
    """Find the dependencies of a node."""
    if node.kind == 'variable':
        return set(node.children[0].value)
    elif node.children is None:
        return set()
    deps = set()
    for c in node.children:
        deps = deps.union(_find_deps(c))
    return deps


def _find_exported(program: Node) -> Set[str]:
    """Find the exported dependencies of a program."""
    assert program.kind == 'program'
    exported = set()
    for line in program.children:
        child = line.children[0]
        if child.kind == 'export':
            exported.add(child.children[0].children[0].value)
    return exported
