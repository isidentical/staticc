from __future__ import annotations

import ast
import textwrap

from staticc.flow import FlowAnalyzer, FlowGraph


def parse_and_analyze(source: str) -> tuple[ast.Module, FlowGraph]:
    tree = ast.parse(textwrap.dedent(source))
    analyzer = FlowAnalyzer()
    return tree, analyzer.analyze(tree)


def test_linear_flow():
    source = """
    import ast
    from staticc import Analyzer

    a = 1
    b = c()
    print(a, b)
    """

    tree, graph = parse_and_analyze(source)
    assert len(graph.blocks) == 1

    first_block = graph.blocks[0]
    for node in tree.body:
        assert graph.index(node) == first_block
