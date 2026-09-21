"""Reference resolution for WEBSTER A10."""
from __future__ import annotations
from dataclasses import dataclass
import re
from .task_memory import TaskMemory, TaskMemoryStore
from .conversation_memory import ConversationMemory, ConversationMemoryStore

@dataclass(frozen=True)
class ReferenceResolution:
    resolved: bool
    intent: str
    goal: str
    task_id: str = ""
    confidence: float = 0.0
    reason: str = ""
    source: str = ""
    candidates: tuple[TaskMemory, ...] = ()

class MemoryReferenceResolver:
    """Resolve follow-up references conservatively from session-scoped memory."""

    _REPEAT = re.compile(r"^\s*(?:do|run|repeat|redo)\s+(?:that|it|the last (?:task|calculation)|that (?:again|task))\s*$|^\s*(?:do|run|repeat|redo)\s+(?:that|it)\s+again\s*$", re.I)
    _CONTINUE = re.compile(r"^\s*(?:continue|resume|carry on with)\s+(?:the\s+)?(?:previous|last|earlier)\s+(?:task|job|thing)\s*$|^\s*(?:continue|resume)\s+(?:that|it)\s*$", re.I)
    _RECALL = re.compile(r"^\s*(?:what|which)\s+(?:was|did)\s+(?:that|the)\s+(?:calculation|task|thing)\s+(?:we\s+)?(?:do|did)\s+(?:earlier|before)\??\s*$|^\s*what\s+was\s+that\s+(?:calculation|task)\s+(?:we\s+)?did\s+earlier\??\s*$", re.I)

    def __init__(self, tasks: TaskMemoryStore, conversations: ConversationMemoryStore) -> None:
        self.tasks = tasks
        self.conversations = conversations

    def resolve(self, text: str, session_id: str) -> ReferenceResolution:
        cleaned = " ".join(text.split())
        if self._RECALL.match(cleaned):
            candidates = self._rank_tasks(cleaned, session_id)
            if len(candidates) >= 2 and self._ambiguous(candidates):
                return ReferenceResolution(False, "clarify_task", "", confidence=0.35, reason="Multiple earlier tasks are similarly relevant.", source="task_memory", candidates=tuple(candidates[:3]))
            if candidates:
                task = candidates[0]
                return ReferenceResolution(True, "recall_task", task.goal, task.task_id, 0.96, "Matched explicit earlier-task recall.", "task_memory", tuple(candidates[:3]))
            conv = self.conversations.search("calculation task", session_id, 4)
            if conv:
                return ReferenceResolution(True, "recall_conversation", conv[0].text, confidence=0.70, reason="Found related conversation history.", source="conversation_memory")
            return ReferenceResolution(False, "recall_task", "", reason="No relevant earlier task in this session.")

        if self._REPEAT.match(cleaned):
            candidates = self._rank_tasks(cleaned, session_id, completed_only=True)
            if len(candidates) >= 2 and self._ambiguous(candidates):
                return ReferenceResolution(False, "clarify_task", "", confidence=0.35, reason="Multiple completed tasks are similarly plausible.", source="task_memory", candidates=tuple(candidates[:3]))
            if candidates:
                task = candidates[0]
                return ReferenceResolution(True, "repeat_task", task.goal, task.task_id, 0.97, "Matched the most recent completed task in this session.", "task_memory", tuple(candidates[:3]))
            return ReferenceResolution(False, "repeat_task", "", reason="No completed task is available in this session.")

        if self._CONTINUE.match(cleaned):
            candidates = self._rank_tasks(cleaned, session_id)
            if len(candidates) >= 2 and self._ambiguous(candidates):
                return ReferenceResolution(False, "clarify_task", "", confidence=0.35, reason="Multiple previous tasks are similarly plausible.", source="task_memory", candidates=tuple(candidates[:3]))
            if candidates:
                task = candidates[0]
                return ReferenceResolution(True, "continue_task", task.goal, task.task_id, 0.94, "Matched the most recent task in this session.", "task_memory", tuple(candidates[:3]))
            return ReferenceResolution(False, "continue_task", "", reason="No previous task is available in this session.")
        return ReferenceResolution(False, "", "")

    def _rank_tasks(self, query: str, session_id: str, completed_only: bool = False) -> list[TaskMemory]:
        tasks = [task for task in self.tasks.recent(20) if task.session_id == session_id and (not completed_only or task.status == "completed")]
        if not tasks:
            return []
        terms = {term.lower() for term in re.findall(r"[a-z0-9]+", query.lower()) if len(term) > 2}
        scored: list[tuple[float, int, TaskMemory]] = []
        for index, task in enumerate(tasks):
            haystack = f"{task.goal} {' '.join(task.results)}".lower()
            lexical = sum(term in haystack for term in terms)
            recency = (index + 1) / len(tasks)
            scored.append((lexical + (0.25 * recency), index, task))
        scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
        return [task for _, _, task in scored]

    @staticmethod
    def _ambiguous(candidates: list[TaskMemory]) -> bool:
        if len(candidates) < 2:
            return False
        first, second = candidates[0], candidates[1]
        return first.goal != second.goal and abs(len(first.goal) - len(second.goal)) < 200
