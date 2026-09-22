"""A19 bounded execution audit records for WEBSTER."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import RLock
from typing import Iterable
from .action_router import ActionResult
from .execution_verifier import VerificationResult
from .planning_engine import Plan


@dataclass(frozen=True)
class ExecutionAudit:
    task_id: str
    step_index: int
    description: str
    action_ok: bool
    verified: bool
    verification_status: str
    classification: str
    message: str
    timestamp: str


class ExecutionAuditor:
    """Keeps a small in-memory audit trail for execution reliability."""

    def __init__(self, max_records: int = 200) -> None:
        self.max_records = max(1, max_records)
        self._records: list[ExecutionAudit] = []
        self._lock = RLock()

    def record(
        self,
        task_id: str,
        plan: Plan,
        step_index: int,
        action: ActionResult,
        verification: VerificationResult,
    ) -> ExecutionAudit:
        step = next((item for item in plan.steps if item.index == step_index), None)
        description = step.description if step else ""
        classification = self.classify(action, verification)
        audit = ExecutionAudit(
            task_id, step_index, description[:500], action.ok, verification.ok,
            verification.status, classification, verification.reason[:1000],
            datetime.now(timezone.utc).isoformat(),
        )
        with self._lock:
            self._records.append(audit)
            self._records = self._records[-self.max_records:]
        return audit

    @staticmethod
    def classify(action: ActionResult, verification: VerificationResult) -> str:
        if verification.ok:
            return "verified_success"
        if verification.retryable:
            return "transient_failure"
        if not action.handled:
            return "unhandled"
        if verification.status == "no_observable_result":
            return "false_success"
        if verification.status == "invalid_tool_result":
            return "invalid_result"
        return "execution_failure"

    def recent(self, limit: int = 20) -> tuple[ExecutionAudit, ...]:
        with self._lock:
            return tuple(self._records[-max(0, limit):])

    def failures(self, limit: int = 20) -> tuple[ExecutionAudit, ...]:
        with self._lock:
            values = [item for item in self._records if item.classification != "verified_success"]
            return tuple(values[-max(0, limit):])
