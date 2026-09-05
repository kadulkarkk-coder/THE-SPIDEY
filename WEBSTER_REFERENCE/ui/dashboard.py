"""Dashboard composition model for the WEBSTER desktop shell."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardCard:
    card_id: str
    title: str
    value: str = ""
    visible: bool = True


class Dashboard:
    """Keep dashboard composition independent from rendering code."""

    def __init__(self) -> None:
        self._cards: dict[str, DashboardCard] = {}

    def add(self, card: DashboardCard) -> DashboardCard:
        if not card.card_id.strip():
            raise ValueError("card_id must not be empty")
        self._cards[card.card_id] = card
        return card

    def remove(self, card_id: str) -> None:
        self._cards.pop(card_id, None)

    def visible(self) -> tuple[DashboardCard, ...]:
        return tuple(card for card in self._cards.values() if card.visible)

    def snapshot(self) -> tuple[DashboardCard, ...]:
        return tuple(self._cards.values())
