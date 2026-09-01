from __future__ import annotations

import json
import os
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

from .analyze import analyze_image, assign_story_roles
from .director import recommend_expression_profile, recommend_systems
from .expression_profiles import expression_profile_names
from .model import SceneCard, load_cards, save_cards
from .narrative_systems import resolve_narrative_system
from .prompt_compiler import compile_manifest
from .readiness import assess_direction_readiness
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
    selected_recommendation = next(item for item in recommendations if item.system == selected_system)
    alternatives = [item for item in recommendations if item.system != selected_system]
    nearest = alternatives[0] if alternatives else None
    score_gap = selected_recommendation.score - nearest.score if nearest else 1.0
    ambiguous = bool(
        system == "auto"
        and nearest
        and selected_recommendation.score >= .8
        and nearest.score >= .8
        and abs(score_gap) < .06
    )
    return {
        "system": selected_system,
        "system_selection": system_selection,
        "expression_profile": selected_profile,
        "profile_selection": "automatic-explicit-brief" if expression_profile == "auto" and selected_profile != "source-led" else "automatic-safe-default" if expression_profile == "auto" else "user-selected",
        "profile_reason": profile_recommendation.reason if expression_profile == "auto" else "The user selected this compatible Expression Profile.",
        "system_score": selected_recommendation.score,
        "score_gap_to_nearest": round(score_gap, 3),
        "needs_route_confirmation": ambiguous,
        "recommendations": [asdict(item) for item in recommendations[:3]],
    }


def run_direct(
    photos: list[Path],
    *,
    output_dir: Path,
    prepared_story: Path | None = None,
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

    analyzed_cards = [analyze_image(path) for path in resolved_photos]
    prepared_story_sha256: str | None = None
    if prepared_story is not None:
        prepared_story = prepared_story.expanduser().resolve()
        prepared_story_sha256 = sha256(prepared_story.read_bytes()).hexdigest()
        cards = load_cards(prepared_story)
        if len(cards) != len(resolved_photos):
            raise ValueError(
                f"Prepared story contains {len(cards)} Scene Card(s), but {len(resolved_photos)} source photo(s) were supplied"
            )
        prepared_sources = [Path(card.source).expanduser().resolve() for card in cards]
        if prepared_sources != resolved_photos:
            raise ValueError("Prepared story sources must match the supplied photos in the same order")
        for card, analyzed in zip(cards, analyzed_cards):
            card.width = analyzed.width
            card.height = analyzed.height
            card.palette = analyzed.palette
            card.brightness = analyzed.brightness
            card.saturation = analyzed.saturation
            card.orientation = analyzed.orientation
        if reorder:
            cards = assign_story_roles(cards, reorder=True)
    else:
        cards = assign_story_roles(analyzed_cards, reorder=reorder)
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
    readiness = assess_direction_readiness(cards)
    manifest = compile_manifest(
        cards,
        route["system"],
        aspect_ratio=aspect_ratio,
        expression_profile=route["expression_profile"],
        source_root=output_dir,
        story_path="story.json",
    )
    generation_ready = readiness["generation_ready"] and not route["needs_route_confirmation"]
    manifest["route_decision"] = {
        "system": route["system"],
        "expression_profile": route["expression_profile"],
        "system_selection": route["system_selection"],
        "profile_selection": route["profile_selection"],
        "needs_route_confirmation": route["needs_route_confirmation"],
    }
    manifest["generation_ready"] = generation_ready

    summary = {
        "artifact_type": "direct-run-summary",
        "schema_version": DIRECT_RUN_SCHEMA_VERSION,
        "created_at": _utc_now(),
        "source_count": len(cards),
        "source_mode": manifest["source_mode"],
        "brief": brief.strip(),
        "prepared_story": {
            "provided": prepared_story is not None,
            "sha256": prepared_story_sha256,
        },
        "route": route,
        "direction_readiness": readiness,
        "outputs": {
            "scene_cards": "story.json",
            "prompt_manifest": "prompt-manifest.json",
            "analysis_workprint": "workprint.svg",
            "workprint_layout_family": WORKPRINT_STYLES[route["system"]],
        },
        "generation": {
            "status": (
                "prompt-ready"
                if generation_ready
                else "needs-route-confirmation"
                if route["needs_route_confirmation"] and readiness["generation_ready"]
                else "needs-semantic-direction"
            ),
            "remote_generation_performed": False,
            "workprint_is_directed_after": False,
            "next_step": (
                "Review the Scene Cards and Prompt Manifest. Before remote generation, record provider-, purpose-, and file-specific consent."
                if generation_ready
                else "Choose a Narrative System explicitly, then rerun direct before requesting upload consent."
                if route["needs_route_confirmation"] and readiness["generation_ready"]
                else "Complete the missing semantic Scene Card fields, then rerun direct with --scene-cards before requesting upload consent."
            ),
        },
    }
    token = uuid.uuid4().hex
    temporary = {
        name: output_dir / f".{name}.{token}.tmp"
        for name in DIRECT_OUTPUT_NAMES
    }
    try:
        save_cards(cards, temporary["story.json"])
        _write_json(temporary["prompt-manifest.json"], manifest)
        render_svg(
            load_cards(temporary["story.json"]),
            temporary["workprint.svg"],
            WORKPRINT_STYLES[route["system"]],
            False,
            "workprint",
            allowed_source_root=output_dir,
            display_name=manifest["system_display_name"],
            subtitle=f"SYSTEM {route['system']} · PROFILE {route['expression_profile']} · ANALYSIS WORKPRINT",
        )
        _write_json(temporary["run-summary.json"], summary)
        for name in DIRECT_OUTPUT_NAMES:
            os.replace(temporary[name], targets[name])
    finally:
        for path in temporary.values():
            if path.exists() and path.is_file() and not path.is_symlink():
                path.unlink()
    return summary
