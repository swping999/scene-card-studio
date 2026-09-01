from __future__ import annotations

from typing import Any

from .model import SceneCard


DEFAULT_DIRECTOR_NOTE = "Preserve the observed scene and let sequencing carry the meaning."


def _is_placeholder(value: str, placeholders: set[str]) -> bool:
    return not value.strip() or value.strip().casefold() in placeholders


def assess_direction_readiness(cards: list[SceneCard]) -> dict[str, Any]:
    """Report whether Scene Cards contain enough semantic evidence for synthesis.

    Low-level image statistics are useful for routing and workprints, but they do
    not identify the subject or authorize transformations.  This check keeps a
    heuristic card from being presented as presentation-ready art direction.
    """

    card_results: list[dict[str, Any]] = []
    for index, card in enumerate(cards):
        missing: list[str] = []
        if not any(value.strip() for value in card.observation.subjects):
            missing.append("observation.subjects")
        if _is_placeholder(card.observation.dominant_gesture, {"still"}):
            missing.append("observation.dominant_gesture")
        if _is_placeholder(card.interpretation.narrative_intent, {"observation"}):
            missing.append("interpretation.narrative_intent")
        if _is_placeholder(card.direction.director_note, {DEFAULT_DIRECTOR_NOTE.casefold()}):
            missing.append("direction.director_note")
        if _is_placeholder(card.direction.layout_emphasis, {"photograph"}):
            missing.append("direction.layout_emphasis")
        if not any(value.strip() for value in card.transformation.must_preserve):
            missing.append("transformation.must_preserve")
        if not any(value.strip() for value in card.transformation.may_transform):
            missing.append("transformation.may_transform")
        card_results.append({
            "source_index": index,
            "source": card.source,
            "ready": not missing,
            "missing_fields": missing,
            "analysis_method": card.interpretation.method,
        })

    ready = bool(cards) and all(item["ready"] for item in card_results)
    return {
        "schema_version": "1.0",
        "status": "generation-ready" if ready else "needs-semantic-direction",
        "generation_ready": ready,
        "card_count": len(cards),
        "cards": card_results,
        "required_semantic_fields": [
            "observation.subjects",
            "observation.dominant_gesture",
            "interpretation.narrative_intent",
            "direction.director_note",
            "direction.layout_emphasis",
            "transformation.must_preserve",
            "transformation.may_transform",
        ],
    }
