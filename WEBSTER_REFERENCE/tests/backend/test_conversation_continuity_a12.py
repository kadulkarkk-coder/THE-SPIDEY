"""A12 conversational continuity tests."""
from pathlib import Path
from WEBSTER_REFERENCE.intelligence.conversation_continuity import ConversationContinuity
from WEBSTER_REFERENCE.intelligence.task_memory import TaskMemoryStore

def test_result_and_pronoun_followup(tmp_path: Path) -> None:
    store = TaskMemoryStore(tmp_path / "tasks.json")
    store.remember("t1", "calculate 12 * 7", "completed", ["84"], session_id="s")
    continuity = ConversationContinuity(store)
    result = continuity.resolve("What was the result?", "s")
    assert result.resolved and result.text == "84"
    follow = continuity.resolve("multiply it by 3", "s")
    assert follow.resolved and follow.text == "84 * 3"
    assert follow.source_task_id == "t1"

def test_other_session_cannot_supply_pronoun_reference(tmp_path: Path) -> None:
    store = TaskMemoryStore(tmp_path / "tasks.json")
    store.remember("t1", "calculate 12 * 7", "completed", ["84"], session_id="other")
    continuity = ConversationContinuity(store)
    assert not continuity.resolve("multiply it by 3", "s").resolved

def test_non_numeric_task_is_not_guessed(tmp_path: Path) -> None:
    store = TaskMemoryStore(tmp_path / "tasks.json")
    store.remember("t1", "check system status", "completed", ["healthy"], session_id="s")
    continuity = ConversationContinuity(store)
    assert not continuity.resolve("multiply it by 3", "s").resolved
