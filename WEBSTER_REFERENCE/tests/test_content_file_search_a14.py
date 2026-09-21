"""A14 tests for content-first file understanding and natural-language search intent."""
from pathlib import Path

from WEBSTER_REFERENCE.intelligence.content_file_index import ContentFileIndex
from WEBSTER_REFERENCE.intelligence.file_search_intent import FileSearchIntentParser


def test_search_uses_file_content_not_filename(tmp_path: Path) -> None:
    (tmp_path / "random_notes.txt").write_text(
        "Photosynthesis converts light energy into chemical energy in plants.",
        encoding="utf-8",
    )
    (tmp_path / "unrelated.txt").write_text("Basketball training schedule.", encoding="utf-8")
    index = ContentFileIndex([tmp_path])
    index.refresh()
    results = index.search("light energy chemical energy plants")
    assert results
    assert results[0].path.endswith("random_notes.txt")
    assert "photosynthesis" in results[0].excerpt.lower()


def test_parser_extracts_content_query() -> None:
    intent = FileSearchIntentParser().parse("find a file about photosynthesis and chlorophyll")
    assert intent.is_search
    assert "photosynthesis" in intent.query
