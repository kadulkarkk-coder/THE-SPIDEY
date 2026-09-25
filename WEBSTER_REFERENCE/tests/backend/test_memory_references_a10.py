"""A10 memory reference resolution tests."""
from pathlib import Path
from WEBSTER_REFERENCE.intelligence.conversation_memory import ConversationMemoryStore
from WEBSTER_REFERENCE.intelligence.memory_reference_resolver import MemoryReferenceResolver
from WEBSTER_REFERENCE.intelligence.task_memory import TaskMemoryStore

def build(tmp_path: Path):
    tasks = TaskMemoryStore(tmp_path / "tasks.json")
    conversations = ConversationMemoryStore(tmp_path / "conversation.json")
    return tasks, conversations, MemoryReferenceResolver(tasks, conversations)

def test_repeat_resolves_only_current_session(tmp_path: Path) -> None:
    tasks, conversations, resolver = build(tmp_path)
    tasks.remember("old", "calculate 99 * 99", "completed", ["9801"], session_id="other")
    tasks.remember("current", "calculate 12 * 7", "completed", ["84"], session_id="current")
    result = resolver.resolve("Do that again", "current")
    assert result.resolved and result.intent == "repeat_task"
    assert result.goal == "calculate 12 * 7"

def test_recall_finds_earlier_task(tmp_path: Path) -> None:
    tasks, conversations, resolver = build(tmp_path)
    tasks.remember("t1", "calculate 12 * 7", "completed", ["84"], session_id="s1")
    result = resolver.resolve("What was that calculation we did earlier?", "s1")
    assert result.resolved and result.intent == "recall_task"
    assert result.goal == "calculate 12 * 7"

def test_continue_uses_previous_failed_task(tmp_path: Path) -> None:
    tasks, conversations, resolver = build(tmp_path)
    tasks.remember("t1", "calculate 2 + 3", "failed", [], "step failed", "s1")
    result = resolver.resolve("continue the previous task", "s1")
    assert result.resolved and result.intent == "continue_task"
    assert result.goal == "calculate 2 + 3"

def test_unrelated_session_does_not_resolve(tmp_path: Path) -> None:
    tasks, conversations, resolver = build(tmp_path)
    tasks.remember("t1", "calculate 12 * 7", "completed", ["84"], session_id="other")
    result = resolver.resolve("Do that again", "s1")
    assert not result.resolved
