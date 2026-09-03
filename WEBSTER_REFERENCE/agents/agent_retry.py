"""Bounded retry policy for recoverable agent failures."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class RetryPolicy:
    max_attempts: int = 2
    def should_retry(self, attempt: int, *, recoverable: bool = True) -> bool:
        return recoverable and 0 <= attempt < max(1, self.max_attempts)
