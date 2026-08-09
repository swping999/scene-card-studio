from __future__ import annotations

from dataclasses import dataclass

from .model import SceneCard


@dataclass(frozen=True)
class Recommendation:
    system: str
    score: float
    reason: str


def recommend_systems(cards: list[SceneCard]) -> list[Recommendation]:
    if not cards:
        return []
    gestures = " ".join(card.observation.dominant_gesture for card in cards).lower()
    intents = " ".join(card.direction.narrative_intent for card in cards).lower()
    average_saturation = sum(card.saturation for card in cards) / len(cards)
    results = [
        Recommendation("editorial-sequence", .72, "A flexible sequence keeps photographs primary and makes story roles legible."),
        Recommendation("memory-atlas", .84 if any(word in gestures + intents for word in ("journey", "route", "departure", "distance")) else .58,
                       "Spatial movement and transitions can become a visible route through the sequence."),
        Recommendation("field-log", .78 if average_saturation < .35 else .62,
                       "Restrained color and observational detail suit a documentary record."),
    ]
    return sorted(results, key=lambda item: item.score, reverse=True)
