"""A20 bounded self-correction decisions for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from .execution_verifier import VerificationResult
from .execution_audit import ExecutionAudit


@dataclass(frozen=True)
class RecoveryDecision:
    action: str
    reason: str
    safe: bool
    user_message: str

    def as_dict(self) -> dict[str, object]:
        return {
            "action": self.action,
            "reason": self.reason,
            "safe": self.safe,
            "user_message": self.user_message,
        }


class SelfCorrection:
    """Selects only bounded, non-destructive recovery actions."""

    def decide(
        self,
        verification: VerificationResult,
        audit: ExecutionAudit | None = None,
        *,
        attempts: int = 1,
    ) -> RecoveryDecision:
        if verification.ok:
            return RecoveryDecision(
                "accept", "verification passed", True,
                "The result was verified successfully.",
            )
        if verification.retryable and attempts < 2:
            return RecoveryDecision(
                "retry", "transient failure within retry budget", True,
                "The step encountered a temporary problem; WEBSTER will retry it once.",
            )
        if verification.status in {"no_observable_result", "invalid_tool_result"}:
            return RecoveryDecision(
                "stop", "result cannot be safely verified", True,
                "WEBSTER stopped because the result could not be verified safely.",
            )
        if audit and audit.classification == "unhandled":
            return RecoveryDecision(
                "stop", "required action was not handled", True,
                "WEBSTER stopped because the requested action was not available.",
            )
        return RecoveryDecision(
            "stop", "no bounded safe recovery is available", True,
            "WEBSTER stopped instead of claiming the task was completed.",
        )
