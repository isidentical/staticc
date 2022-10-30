from __future__ import annotations

import ast
import typing
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import singledispatchmethod

from staticc.analyzers import TreeAnalyzer


class Continuation(Enum):
    RETURN = auto()


@dataclass
class BasicBlock:
    """Represents a list of nodes that will be executed linearly without
    any branching or continuation (raise/return/break etc.). If the final
    node has continuation properties, then `continuation_type` will be
    set."""

    nodes: list[ast.stmt] = field(default_factory=list)
    continuation_type: Continuation | None = None

    def push(self, node: ast.stmt) -> None:
        self.nodes.append(node)


class BlockEdge(typing.NamedTuple):
    """Jump between two blocks."""

    from_: BasicBlock
    to_: BasicBlock

    when: str | None = None


@dataclass
class FlowGraph:
    """Represents a graph of basic blocks."""

    blocks: list[BasicBlock] = field(default_factory=list)
    edges: list[BlockEdge] = field(default_factory=list)

    def index(self, node: ast.stmt) -> BasicBlock:
        """Find the block that contains the given node."""
        for block in self.blocks:
            if node in block.nodes:
                return block
        else:
            raise ValueError(
                f"Node {node} not found in graph. Perhaps it does not belong to this"
                " tree?"
            )


@dataclass
class FlowAnalyzer(TreeAnalyzer[FlowGraph]):
    graph: FlowGraph = field(default_factory=FlowGraph)
    _stack: list[BasicBlock] = field(default_factory=list)

    @property
    def active_block(self) -> BasicBlock:
        """Return the active block."""
        return self._stack[-1]

    def add_edge(
        self,
        from_: BasicBlock,
        to_: BasicBlock,
        /,
        when: str | None = None,
    ) -> None:
        """Record a new edge between two blocks."""
        self.graph.edges.append(BlockEdge(from_, to_, when))

    def push_block(self) -> BasicBlock:
        """Activate a new basic block."""
        new_block = BasicBlock()
        self._stack.append(new_block)
        self.graph.blocks.append(new_block)
        return new_block

    def analyze(self, node: ast.Module) -> FlowGraph:
        """Return the execution and control flow graph for
        the given module."""

        # Each module's execution starts with a fresh block (so all
        # the non-control flow statements in the body will have a place
        # to go).
        self.push_block()
        self.visit_statements(*node.body)
        return self.graph

    def visit_statements(self, *statements: ast.stmt) -> None:
        """Visit the given statements in a linear order."""
        for statement in statements:
            self.visit(statement)

    @singledispatchmethod
    def visit(self, node: ast.stmt) -> None:
        # Any statement that does not affect the flow of the program
        # will be added to the current block.
        self.active_block.push(node)
