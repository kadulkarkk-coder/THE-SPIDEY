"""A18 execution verification and bounded recovery for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
import re
from .action_router import ActionResult


@dataclass(frozen=True)
class VerificationResult:
    ok: bool
    status: str
    reason: str
    retryable: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "status": self.status,
            "reason": self.reason,
            "retryable": self.retryable,
        }


class ExecutionVerifier:
    """Checks observable action outcomes before a task may be marked complete."""

    _TRANSIENT = re.compile(r"\b(?:timeout|temporar(?:y|ily)|busy|unavailable|try again|connection)\b", re.I)

    def verify(self, action: ActionResult) -> VerificationResult:
        if not action.handled:
            return VerificationResult(False, "not_handled", "The requested step was not handled.")
        if not action.ok:
            retryable = bool(self._TRANSIENT.search(action.message))
            return VerificationResult(False, "failed", action.message or "The action reported failure.", retryable)
        if not str(action.message).strip():
            return VerificationResult(False, "no_observable_result", "The action reported success without an observable result.")
        if action.kind == "tool" and not isinstance(action.data, dict):
            return VerificationResult(False, "invalid_tool_result", "The tool did not return structured execution metadata.")
        return VerificationResult(True, "verified", "The action returned a valid observable success result.")

    @staticmethod
    def can_retry(result: VerificationResult, attempts: int) -> bool:
        return result.retryable and attempts < 2
