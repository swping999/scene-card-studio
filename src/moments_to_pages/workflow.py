from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .analyze import analyze_image, assign_story_roles
from .director import recommend_expression_profile, recommend_systems
from .expression_profiles import expression_profile_names
from .model import SceneCard, load_cards, save_cards
from .narrative_systems import resolve_narrative_system
from .prompt_compiler import compile_manifest
from .render import render_svg

DIRECT_RUN_SCHEMA_VERSION = "1.0"
DIRECT_OUTPUT_NAMES = ("story.json", "prompt-manifest.json", "workprint.svg", "run-summary.json")

WORKPRINT_STYLES = {
    "cinematic-storyboard": "editorial-sequence",
    "memory-atlas": "memory-atlas",
    "family-archive": "family-archive",
    "minimal-editorial": "editorial-minimal",
    "editorial-sequence": "editorial-sequence",
    "field-log": "field-log",
    "museum-catalogue": "field-log",
    "travel-journal": "memory-atlas",
    "street-reportage": "field-log",
    "fashion-editorial": "editorial-minimal",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def _apply_user_brief(cards: list[SceneCard], brief: str) -> None:
    cleaned = brief.strip()
    if not cleaned:
        return
    for card in cards:
        card.interpretation.narrative_intent = cleaned
        card.interpretation.confidence = 1.0
        card.interpretation.method = "user-supplied-brief"
        card.direction.director_note = f"Follow the user-supplied art-direction brief without treating it as photographic fact: {cleaned}"


def select_direct_route(
    cards: list[SceneCard],
    *,
    brief: str = "",
    system: str = "auto",
    expression_profile: str = "auto",
) -> dict[str, Any]:
    recommendations = recommend_systems(cards, brief=brief)
    if not recommendations:
        raise ValueError("At least one source photo is required")
    system_selection = "user-selected"
    if system == "auto" and expression_profile != "auto":
        compatible_recommendations = [
            item for item in recommendations
            if expression_profile in expression_profile_names(item.system)
        ]
        if not compatible_recommendations:
            raise ValueError(f"Unknown expression profile or no compatible Narrative System: {expression_profile!r}")
        selected_system = compatible_recommendations[0].system
        system_selection = "automatic-compatible-with-profile"
    elif system == "auto":
        explicit_profile_routes = [
            (item, recommend_expression_profile(item.system, cards, brief))
            for item in recommendations
        ]
        explicit_profile_routes = [
            item for item in explicit_profile_routes if item[1].profile != "source-led"
        ]
        selected_system = explicit_profile_routes[0][0].system if explicit_profile_routes else recommendations[0].system
        system_selection = "automatic"
    else:
        selected_system = system
    resolve_narrative_system(selected_system)
    profile_recommendation = recommend_expression_profile(selected_system, cards, brief)
    selected_profile = profile_recommendation.profile if expression_profile == "auto" else expression_profile
    compatible = expression_profile_names(selected_system)
    if selected_profile not in compatible:
        choices = ", ".join(compatible)
        raise ValueError(
            f"Expression profile {selected_profile!r} is not compatible with {selected_system}; choose: {choices}"
        )
    return {
        "system": selected_system,
        "system_selection": system_selection,
        "expression_profile": selected_profile,
        "profile_selection": "automatic-explicit-brief" if expression_profile == "auto" and selected_profile != "source-led" else "automatic-safe-default" if expression_profile == "auto" else "user-selected",
        "profile_reason": profile_recommendation.reason if expression_profile == "auto" else "The user selected this compatible Expression Profile.",
        "recommendations": [asdict(item) for item in recommendations[:3]],
    }


def run_direct(
    photos: list[Path],
    *,
    output_dir: Path,
    brief: str = "",
    system: str = "auto",
    expression_profile: str = "auto",
    aspect_ratio: str = "source",
    reorder: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    if not photos:
        raise ValueError("At least one source photo is required")
    resolved_photos = [photo.expanduser().resolve() for photo in photos]
    for photo in resolved_photos:
        if not photo.is_file():
            raise FileNotFoundError(f"Source photo does not exist or is not a file: {photo}")

    output_dir = output_dir.expanduser().resolve()
    targets = {name: output_dir / name for name in DIRECT_OUTPUT_NAMES}
    existing = [path for path in targets.values() if path.exists() or path.is_symlink()]
    if existing and not force:
        names = ", ".join(path.name for path in existing)
        raise FileExistsError(f"Direct output already exists ({names}); choose another directory or pass --force")
    unsafe_targets = [path for path in existing if path.is_symlink() or not path.is_file()]
    if unsafe_targets:
        names = ", ".join(path.name for path in unsafe_targets)
        raise PermissionError(f"Refusing to replace non-regular direct output target(s): {names}")

    cards = assign_story_roles([analyze_image(path) for path in resolved_photos], reorder=reorder)
    _apply_user_brief(cards, brief)
    route = select_direct_route(
        cards,
        brief=brief,
        system=system,
        expression_profile=expression_profile,
    )

    # The directory must exist before source_root / "../photo" can be resolved
    # portably by all supported filesystems. No run artifact is written yet.
    output_dir.mkdir(parents=True, exist_ok=True)
    for card in cards:
        card.source = Path(os.path.relpath(Path(card.source).resolve(), output_dir)).as_posix()
    manifest = compile_manifest(
        cards,
        route["system"],
        aspect_ratio=aspect_ratio,
        expression_profile=route["expression_profile"],
        source_root=output_dir,
        story_path="story.json",
    )

    save_cards(cards, targets["story.json"])
    _write_json(targets["prompt-manifest.json"], manifest)

    render_svg(
        load_cards(targets["story.json"]),
        targets["workprint.svg"],
        WORKPRINT_STYLES[route["system"]],
        False,
        "workprint",
        allowed_source_root=output_dir,
    )

    summary = {
        "artifact_type": "direct-run-summary",
        "schema_version": DIRECT_RUN_SCHEMA_VERSION,
        "created_at": _utc_now(),
        "source_count": len(cards),
        "source_mode": manifest["source_mode"],
        "brief": brief.strip(),
        "route": route,
        "outputs": {
            "scene_cards": "story.json",
            "prompt_manifest": "prompt-manifest.json",
            "analysis_workprint": "workprint.svg",
        },
        "generation": {
            "status": "prompt-ready",
            "remote_generation_performed": False,
            "workprint_is_directed_after": False,
            "next_step": "Review the Scene Cards and Prompt Manifest. Before remote generation, record provider-, purpose-, and file-specific consent.",
        },
    }
    _write_json(targets["run-summary.json"], summary)
    return summary
