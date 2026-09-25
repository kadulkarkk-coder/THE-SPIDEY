"""A8 task-memory tests."""
from pathlib import Path
from WEBSTER_REFERENCE.intelligence.task_memory import TaskMemoryStore

def test_memory_persists_and_retrieves(tmp_path: Path) -> None:
    path = tmp_path / "memory.json"
    first = TaskMemoryStore(path)
    first.remember("t1", "calculate 12 * 7", "completed", ["84"])
    second = TaskMemoryStore(path)
    matches = second.find("12 7")
    assert matches and matches[0].task_id == "t1" and matches[0].results == ("84",)

def test_memory_is_bounded(tmp_path: Path) -> None:
    store = TaskMemoryStore(tmp_path / "memory.json", max_records=2)
    store.remember("1", "one", "completed")
    store.remember("2", "two", "completed")
    store.remember("3", "three", "completed")
    assert [x.task_id for x in store.recent()] == ["2", "3"]
