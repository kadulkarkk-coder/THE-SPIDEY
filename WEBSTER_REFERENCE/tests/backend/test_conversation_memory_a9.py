"""A9 conversation memory tests."""
from pathlib import Path
from WEBSTER_REFERENCE.intelligence.conversation_memory import ConversationMemoryStore

def test_conversation_persists_and_searches(tmp_path: Path) -> None:
    path = tmp_path / "conversation.json"
    first = ConversationMemoryStore(path)
    first.remember("s1", "user", "What is my project name?")
    first.remember("s1", "assistant", "WEBSTER")
    second = ConversationMemoryStore(path)
    matches = second.search("project name", "s1")
    assert matches and matches[0].role == "user"

def test_conversation_is_bounded(tmp_path: Path) -> None:
    store = ConversationMemoryStore(tmp_path / "conversation.json", max_records=2)
    store.remember("s", "user", "one")
    store.remember("s", "user", "two")
    store.remember("s", "user", "three")
    assert [x.text for x in store.recent("s")] == ["two", "three"]
