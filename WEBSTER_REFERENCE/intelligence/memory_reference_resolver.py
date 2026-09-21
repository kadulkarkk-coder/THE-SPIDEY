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
            task = self._best_task(session_id)
            if task:
                return ReferenceResolution(True, "recall_task", task.goal, task.task_id, 0.96, "Matched explicit earlier-task recall.", "task_memory")
            conv = self.conversations.search("calculation task", session_id, 4)
            if conv:
                return ReferenceResolution(True, "recall_conversation", conv[0].text, confidence=0.70, reason="Found related conversation history.", source="conversation_memory")
            return ReferenceResolution(False, "recall_task", "", reason="No relevant earlier task in this session.")

        if self._REPEAT.match(cleaned):
            task = self._best_task(session_id, completed_only=True)
            if task:
                return ReferenceResolution(True, "repeat_task", task.goal, task.task_id, 0.97, "Matched the most recent completed task in this session.", "task_memory")
            return ReferenceResolution(False, "repeat_task", "", reason="No completed task is available in this session.")

        if self._CONTINUE.match(cleaned):
            task = self._best_task(session_id)
            if task:
                return ReferenceResolution(True, "continue_task", task.goal, task.task_id, 0.94, "Matched the most recent task in this session.", "task_memory")
            return ReferenceResolution(False, "continue_task", "", reason="No previous task is available in this session.")
        return ReferenceResolution(False, "", "")

    def _best_task(self, session_id: str, completed_only: bool = False) -> TaskMemory | None:
        for task in reversed(self.tasks.recent(20)):
            if task.session_id and task.session_id != session_id:
                continue
            if completed_only and task.status != "completed":
                continue
            return task
        return None
