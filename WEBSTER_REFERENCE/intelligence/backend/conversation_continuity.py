"""Reference-aware conversational continuity for WEBSTER A12."""
from __future__ import annotations
from dataclasses import dataclass
import re
from .task_memory import TaskMemoryStore, TaskMemory

@dataclass(frozen=True)
class ContinuityResolution:
    resolved: bool
    intent: str
    text: str = ""
    source_task_id: str = ""
    confidence: float = 0.0
    reason: str = ""

class ConversationContinuity:
    """Resolve short follow-ups against the most relevant active-session task."""
    _RESULT = re.compile(r"^\s*(?:what(?:'s| is| was)\s+)?(?:the\s+)?(?:result|answer)\s*(?:of\s+that)?\??\s*$", re.I)
    _VERB = re.compile(r"^\s*(?:now\s+)?(multiply|divide|add|subtract|plus|minus|times)\s+(?:it|that|the\s+(?:number|result))\s+(?:by\s+)?(.+?)\s*$", re.I)

    def __init__(self, tasks: TaskMemoryStore) -> None:
        self.tasks = tasks

    def resolve(self, text: str, session_id: str) -> ContinuityResolution:
        task = self._latest(session_id)
        if not task:
            return ContinuityResolution(False, "")
        result = self._numeric_result(task)
        cleaned = " ".join(text.split())
        if self._RESULT.match(cleaned) and result is not None:
            return ContinuityResolution(True, "recall_result", str(result), task.task_id, .98, "Resolved result from latest session task.")
        match = self._VERB.match(cleaned)
        if match and result is not None:
            try:
                operand = float(match.group(2).strip())
                operand = int(operand) if operand.is_integer() else operand
            except ValueError:
                return ContinuityResolution(False, "")
            op = {"multiply":"*","times":"*","divide":"/","add":"+","plus":"+","subtract":"-","minus":"-"}.get(match.group(1).lower())
            if op:
                return ContinuityResolution(True, "followup_calculation", f"{result} {op} {operand}", task.task_id, .96, "Resolved pronoun to latest task result.")
        return ContinuityResolution(False, "")

    def _latest(self, session_id: str) -> TaskMemory | None:
        for task in reversed(self.tasks.recent(20)):
            if task.session_id == session_id:
                return task
        return None

    @staticmethod
    def _numeric_result(task: TaskMemory) -> float | int | None:
        for value in reversed(task.results):
            match = re.search(r"(?<![\d.])-?\d+(?:\.\d+)?(?![\d.])", value)
            if match:
                number = float(match.group(0))
                return int(number) if number.is_integer() else number
        return None
