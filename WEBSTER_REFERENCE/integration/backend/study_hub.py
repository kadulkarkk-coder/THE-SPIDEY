"""Lightweight Study Hub domain model for Windows and Android clients."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class StudyItem:
    title: str
    subject: str = ""
    chapter: str = ""
    kind: str = "note"
    tags: tuple[str, ...] = field(default_factory=tuple)


class StudyHub:
    """Local-first study collection; UI and AI explanation layers remain separate."""

    def __init__(self) -> None:
        self._items: list[StudyItem] = []

    def add(self, item: StudyItem) -> None:
        if not item.title.strip():
            raise ValueError("study item title must not be empty")
        self._items.append(item)

    def items(self, subject: str | None = None) -> tuple[StudyItem, ...]:
        if subject is None:
            return tuple(self._items)
        return tuple(item for item in self._items if item.subject.casefold() == subject.casefold())
