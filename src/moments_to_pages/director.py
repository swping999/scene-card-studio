from __future__ import annotations

from dataclasses import dataclass
import re

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
    intents = " ".join(card.interpretation.narrative_intent for card in cards).lower()
    subjects = " ".join(" ".join(card.observation.subjects) for card in cards).lower()
    tones = " ".join(" ".join(card.interpretation.emotional_tone) for card in cards).lower()
    notes = " ".join(card.direction.director_note for card in cards).lower()
    evidence = " ".join((gestures, intents, subjects, tones, notes))
    tokens = set(re.findall(r"[a-z]+", evidence))
    average_saturation = sum(card.saturation for card in cards) / len(cards)
    cinematic_words = ("waiting", "departure", "night", "rain", "reflection", "window", "vehicle", "movement", "pause")
    minimal_words = ("object", "material", "linen", "chair", "cup", "mug", "ceramic", "fabric", "surface", "fold")
    cinematic_matches = sum(word in tokens for word in cinematic_words)
    minimal_matches = sum(word in tokens for word in minimal_words)
    results = [
        Recommendation("editorial-sequence", .72, "A flexible sequence keeps photographs primary and makes story roles legible."),
        Recommendation("memory-atlas", .84 if any(word in gestures + intents for word in ("journey", "route", "departure", "distance")) else .58,
                       "Spatial movement and transitions can become a visible route through the sequence."),
        Recommendation("field-log", .78 if average_saturation < .35 else .62,
                       "Restrained color and observational detail suit a documentary record."),
        Recommendation("family-archive", .86 if any(word in gestures + intents for word in ("family", "care", "inherit", "home", "shared")) else .52,
                       "Repeated domestic gestures and relationships can be read as a family record."),
        Recommendation("cinematic-storyboard", .88 if cinematic_matches >= 2 else .56,
                       "Temporal continuity, motivated light, weather, and shot relationships can carry the sequence."),
        Recommendation("minimal-editorial", .86 if average_saturation < .38 and minimal_matches >= 2 else .54,
                       "Object hierarchy, negative space, light, and material evidence can direct each frame."),
    ]
    return sorted(results, key=lambda item: item.score, reverse=True)
