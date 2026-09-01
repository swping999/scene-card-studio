from __future__ import annotations

from typing import Any

NARRATIVE_SYSTEMS: dict[str, dict[str, Any]] = {
    "cinematic-storyboard": {
        "display_name": "Cinematic Sequence",
        "prompt_mode": "per-source",
        "artifact_mode": "cinematic-sequence",
        "metadata_fields": ("caption", "story_role"),
    },
    "memory-atlas": {
        "display_name": "Memory Atlas",
        "prompt_mode": "synthesis",
        "artifact_mode": "spatial-synthesis",
        "metadata_fields": ("caption", "location", "date"),
    },
    "family-archive": {
        "display_name": "Family Chronicle",
        "prompt_mode": "synthesis",
        "artifact_mode": "archival-synthesis",
        "metadata_fields": ("caption", "date", "collection"),
    },
    "minimal-editorial": {
        "display_name": "Quiet Editorial",
        "prompt_mode": "per-source",
        "artifact_mode": "quiet-editorial",
        "metadata_fields": ("caption",),
    },
    "editorial-sequence": {
        "display_name": "Editorial Rhythm",
        "prompt_mode": "per-source",
        "artifact_mode": "editorial-sequence",
        "metadata_fields": ("caption", "story_role"),
    },
    "field-log": {
        "display_name": "Field Log",
        "prompt_mode": "per-source",
        "artifact_mode": "field-observation",
        "metadata_fields": ("caption", "date", "location", "source_note"),
    },
    "museum-catalogue": {
        "display_name": "Museum Catalogue",
        "prompt_mode": "per-source",
        "artifact_mode": "catalogue-plate",
        "metadata_fields": ("caption", "collection", "catalogue_id", "date", "source_note"),
    },
    "travel-journal": {
        "display_name": "Travel Journal",
        "prompt_mode": "synthesis",
        "artifact_mode": "journey-synthesis",
        "metadata_fields": ("caption", "location", "date", "source_note"),
    },
    "street-reportage": {
        "display_name": "Street Reportage",
        "prompt_mode": "per-source",
        "artifact_mode": "reportage-sequence",
        "metadata_fields": ("caption", "location", "date"),
    },
    "fashion-editorial": {
        "display_name": "Fashion Editorial",
        "prompt_mode": "per-source",
        "artifact_mode": "fashion-sequence",
        "metadata_fields": ("caption", "story_role"),
    },
}


SUPPORTED_SYSTEMS = tuple(NARRATIVE_SYSTEMS)


def resolve_narrative_system(name: str) -> dict[str, Any]:
    if name not in NARRATIVE_SYSTEMS:
        raise ValueError(f"Unsupported prompt system: {name}")
    return {"name": name, **NARRATIVE_SYSTEMS[name]}
