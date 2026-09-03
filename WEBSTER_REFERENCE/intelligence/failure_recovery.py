"""Safe, bounded failure diagnosis and recovery planning for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RecoveryAction(str, Enum):
    RETRY = "retry"
    FALLBACK = "fallback"
    ABORT = "abort"
    ESCALATE = "escalate"


@dataclass(frozen=True)
class Failure:
    operation: str
    message: str
    retryable: bool = False
    attempts: int = 0


@dataclass(frozen=True)
class RecoveryPlan:
    action: RecoveryAction
    reason: str
    next_attempt: int


class FailureRecovery:
    """Chooses conservative recovery actions without executing them automatically."""

    def plan(self, failure: Failure, *, max_retries: int = 2) -> RecoveryPlan:
        limit = max(0, max_retries)
        if failure.retryable and failure.attempts < limit:
            return RecoveryPlan(RecoveryAction.RETRY, "Failure is marked retryable and retry budget remains", failure.attempts + 1)
        if failure.retryable:
            return RecoveryPlan(RecoveryAction.FALLBACK, "Retry budget exhausted; use a safer fallback", failure.attempts)
        return RecoveryPlan(RecoveryAction.ESCALATE, "Failure is not approved for automatic retry", failure.attempts)

    def abort(self, reason: str) -> RecoveryPlan:
        return RecoveryPlan(RecoveryAction.ABORT, reason.strip() or "Operation aborted", 0)
