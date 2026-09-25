from pathlib import Path

from WEBSTER_REFERENCE.intelligence.content_file_index import ContentFileIndex
from WEBSTER_REFERENCE.intelligence.local_retrieval import LocalRetriever


def test_related_concept_retrieval(tmp_path: Path) -> None:
    (tmp_path / "random.txt").write_text(
        "Plants use chlorophyll to convert light energy into glucose.",
        encoding="utf-8",
    )
    (tmp_path / "other.txt").write_text("A football match was scheduled.", encoding="utf-8")
    index = ContentFileIndex([tmp_path])
    index.refresh()
    hits = LocalRetriever(index).retrieve("how do plants make food")
    assert hits
    assert hits[0].path.endswith("random.txt")
    assert hits[0].reason in {"direct content match", "related concept match"}


def test_empty_query_is_safe(tmp_path: Path) -> None:
    index = ContentFileIndex([tmp_path])
    assert LocalRetriever(index).retrieve("") == ()
