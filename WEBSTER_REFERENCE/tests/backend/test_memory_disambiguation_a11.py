"""A11 contextual disambiguation tests."""
from pathlib import Path
from WEBSTER_REFERENCE.intelligence.conversation_memory import ConversationMemoryStore
from WEBSTER_REFERENCE.intelligence.memory_reference_resolver import MemoryReferenceResolver
from WEBSTER_REFERENCE.intelligence.task_memory import TaskMemoryStore

def build(tmp_path: Path):
    tasks = TaskMemoryStore(tmp_path / "tasks.json")
    conversations = ConversationMemoryStore(tmp_path / "conversation.json")
    return tasks, conversations, MemoryReferenceResolver(tasks, conversations)

def test_generic_reference_clarifies_when_two_tasks_are_plausible(tmp_path: Path) -> None:
    tasks, _, resolver = build(tmp_path)
    tasks.remember("t1", "calculate 12 * 7", "completed", ["84"], session_id="s")
    tasks.remember("t2", "calculate 25 + 18", "completed", ["43"], session_id="s")
    result = resolver.resolve("Do that again", "s")
    assert not result.resolved and result.intent == "clarify_task"
    assert {item.task_id for item in result.candidates} == {"t1", "t2"}

def test_specific_reference_selects_clear_match(tmp_path: Path) -> None:
    tasks, _, resolver = build(tmp_path)
    tasks.remember("t1", "calculate 12 * 7", "completed", ["84"], session_id="s")
    tasks.remember("t2", "calculate 25 + 18", "completed", ["43"], session_id="s")
    result = resolver.resolve("What was the calculation 12 7 we did earlier?", "s")
    assert result.resolved and result.intent == "recall_task"
    assert result.task_id == "t1"

def test_foreign_session_is_never_a_candidate(tmp_path: Path) -> None:
    tasks, _, resolver = build(tmp_path)
    tasks.remember("foreign", "calculate 12 * 7", "completed", ["84"], session_id="other")
    result = resolver.resolve("Do that again", "s")
    assert not result.resolved and result.intent == "repeat_task"
