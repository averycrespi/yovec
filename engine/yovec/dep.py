def graph(program):
    """Graph the dependencies of a program."""
    assert program.kind == 'program'
    deps = {}
    for line in program.children:
        for c in line.children:
            if c.kind.startswith('let'):
                ident = c.children[0].children[0].value
                deps[ident] = _find_deps(c)
    return deps


def _find_deps(node):
    """Find the dependencies of a node."""
    if node.kind == 'variable':
        return set(node.children[0].value)
    elif node.children is None:
        return set()
    d = set()
    for c in node.children:
        d = d.union(_find_deps(c))
    return d
