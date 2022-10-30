from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Generic, TypeVar

ResultT = TypeVar("ResultT")
ExpectedNodeT = TypeVar("ExpectedNodeT", bound=ast.AST)


class _GenericAnalyzer(Generic[ExpectedNodeT, ResultT]):
    def analyze(self, node: ExpectedNodeT) -> ResultT:
        ...


@dataclass
class Analyzer(_GenericAnalyzer[ast.AST, ResultT]):
    """A generic analyzer that can be used for any node in the same
    tree (state)."""

    def analyze(self, node: ast.AST) -> ResultT:
        raise NotImplementedError


@dataclass
class TreeAnalyzer(_GenericAnalyzer[ast.Module, ResultT]):
    """A tree level analyzer that only accepts a module as its input."""

    def analyze(self, node: ast.Module) -> ResultT:
        raise NotImplementedError
