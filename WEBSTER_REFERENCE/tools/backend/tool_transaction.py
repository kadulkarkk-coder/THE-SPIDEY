"""Reversible state boundary for tool operations."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class TransactionResult:
    success: bool
    value: object = None
    error: str | None = None

class ToolTransaction:
    def run(self, action: Callable[[], object], rollback: Callable[[], None] | None = None) -> TransactionResult:
        try:
            return TransactionResult(True, action())
        except Exception as exc:
            if rollback is not None:
                try: rollback()
                except Exception: pass
            return TransactionResult(False, error=f"{exc.__class__.__name__}: {exc}")
