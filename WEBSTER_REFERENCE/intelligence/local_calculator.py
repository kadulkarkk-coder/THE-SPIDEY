"""Dependency-free calculator for simple arithmetic expressions."""
from __future__ import annotations

import ast
import operator


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str) -> float | int | None:
    """Evaluate arithmetic only; names, calls, attributes and containers are rejected."""
    expression = expression.strip().replace("×", "*").replace("÷", "/")
    if not expression or len(expression) > 120:
        return None
    try:
        tree = ast.parse(expression, mode="eval")
        return _eval(tree.body)
    except (ArithmeticError, SyntaxError, ValueError, TypeError, OverflowError):
        return None


def _eval(node: ast.AST) -> float | int:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        if abs(node.value) > 10**12:
            raise ValueError("number too large")
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 12:
            raise ValueError("exponent too large")
        result = _OPERATORS[type(node.op)](left, right)
        if abs(result) > 10**15:
            raise ValueError("result too large")
        return result
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")
