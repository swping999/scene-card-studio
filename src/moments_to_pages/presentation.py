from __future__ import annotations

from hashlib import sha256
from html import escape
import os
from pathlib import Path
from typing import Any
from urllib.parse import quote

from .model import SceneCard
from .narrative_systems import resolve_narrative_system


def _card_metadata(card: SceneCard, index: int, prompt_id: str) -> dict[str, Any]:
    record: dict[str, Any] = {
        "source_index": index,
        "prompt_id": prompt_id,
        "caption": card.caption,
        "story_role": card.story_role,
    }
    for name in ("date", "location", "collection", "catalogue_id", "source_note"):
        value = getattr(card.metadata, name).strip()
        if value:
            record[name] = value
    return record


def build_presentation_contract(cards: list[SceneCard], system: str, prompt_ids: list[str]) -> dict[str, Any]:
    spec = resolve_narrative_system(system)
    if spec["prompt_mode"] == "per-source" and len(prompt_ids) != len(cards):
        raise ValueError(f"{system} presentation contract requires one prompt id per Scene Card")
    if spec["prompt_mode"] == "synthesis" and len(prompt_ids) != 1:
        raise ValueError(f"{system} presentation contract requires one synthesis prompt id")
    entries = [
        _card_metadata(card, index, prompt_ids[index] if len(prompt_ids) > 1 else prompt_ids[0])
        for index, card in enumerate(cards)
    ]
    required = tuple(spec["metadata_fields"])
    missing = sorted({field for field in required for entry in entries if not str(entry.get(field, "")).strip()})
    return {
        "schema_version": "1.0",
        "renderer": "deterministic-overlay",
        "display_name": spec["display_name"],
        "source_mode": "single-photo" if len(cards) == 1 else ("multi-photo-per-source" if spec["prompt_mode"] == "per-source" else "multi-photo-synthesis"),
        "image_generation_text_policy": "no-visible-text",
        "allowed_metadata_fields": list(required),
        "entries": entries,
        "missing_optional_metadata": missing,
        "rules": [
            "Render labels only from the entries in this contract.",
            "Omit missing fields; never infer names, dates, locations, collection data, or catalogue identifiers.",
            "Keep generated image pixels and deterministic typography as separate provenance layers.",
        ],
    }


def render_presentation_svg(manifest: dict[str, Any], output: Path, base: Path | None = None) -> None:
    if manifest.get("artifact_type") != "render-manifest":
        raise ValueError("Presentation rendering requires a Render Manifest produced by bind-outputs")
    if manifest.get("candidate_path_base") != "render-manifest-directory":
        raise ValueError("Render Manifest must declare candidate paths relative to its own directory")
    contract = manifest.get("presentation_contract")
    if not isinstance(contract, dict) or contract.get("renderer") != "deterministic-overlay":
        raise ValueError("Render Manifest has no deterministic presentation_contract")
    if contract.get("image_generation_text_policy") != "no-visible-text":
        raise ValueError("Presentation contract must keep image-generation text disabled")
    prompt_map = {prompt["id"]: prompt for prompt in manifest.get("prompts", [])}
    if not prompt_map:
        raise ValueError("Render Manifest contains no prompts")
    for prompt in prompt_map.values():
        candidate = prompt.get("candidate_output")
        if not isinstance(candidate, dict) or not candidate.get("path") or not candidate.get("sha256"):
            raise ValueError(f"Prompt {prompt.get('id')} has no bound candidate_output")

    prompt_ids = list(prompt_map)
    width = 1200
    section_height = 900
    height = 210 + section_height * len(prompt_ids)
    ink = "#1F211F"
    paper = "#F4F1E9"
    accent = "#5A675F"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{paper}"/>',
        f'<text x="72" y="70" font-family="system-ui,sans-serif" font-size="16" letter-spacing="3" fill="{accent}">SCENE CARD STUDIO · DETERMINISTIC PRESENTATION</text>',
        f'<text x="72" y="132" font-family="system-ui,sans-serif" font-size="46" fill="{ink}">{escape(str(contract.get("display_name", manifest.get("system", ""))))}</text>',
    ]
    entries = contract.get("entries", [])
    base_path = (base or Path.cwd()).resolve()
    for prompt_index, prompt_id in enumerate(prompt_ids):
        prompt = prompt_map[prompt_id]
        candidate = prompt["candidate_output"]
        candidate_path = Path(candidate["path"]).expanduser()
        resolved = candidate_path if candidate_path.is_absolute() else base_path / candidate_path
        if not resolved.exists() or not resolved.is_file():
            raise FileNotFoundError(f"Bound candidate does not exist: {resolved}")
        if sha256(resolved.read_bytes()).hexdigest() != candidate["sha256"]:
            raise ValueError(f"Bound candidate hash changed for {prompt_id}")
        try:
            href = Path(os.path.relpath(resolved.resolve(), output.resolve().parent)).as_posix()
        except ValueError as exc:
            raise ValueError(
                "Bound candidate and presentation must be on the same filesystem so the SVG remains portable"
            ) from exc
        encoded_href = quote(href, safe="/:.")
        y = 190 + prompt_index * section_height
        parts.extend([
            f'<rect x="72" y="{y}" width="1056" height="650" fill="#E4E0D7"/>',
            f'<image href="{encoded_href}" x="72" y="{y}" width="1056" height="650" preserveAspectRatio="xMidYMid meet"/>',
            f'<text x="72" y="{y+700}" font-family="ui-monospace,monospace" font-size="14" fill="{accent}">{escape(prompt_id.upper())} · {escape(candidate["sha256"][:12])}</text>',
        ])
        prompt_entries = [entry for entry in entries if entry.get("prompt_id") == prompt_id]
        labels: list[tuple[str, str]] = []
        for entry in prompt_entries:
            label = f'{int(entry.get("source_index", 0)) + 1:02d} · {entry.get("caption", "").strip()}'
            details = " · ".join(
                str(entry[field]).strip() for field in ("story_role", "location", "date", "collection", "catalogue_id")
                if str(entry.get(field, "")).strip()
            )
            labels.append((label + (f" · {details}" if details else ""), str(entry.get("source_note", "")).strip()))
        row = 0
        for label, note in labels:
            if row >= 4:
                break
            parts.append(f'<text x="72" y="{y+742+row*30}" font-family="system-ui,sans-serif" font-size="20" fill="{ink}">{escape(label[:96])}</text>')
            row += 1
            if note and row < 4:
                parts.append(f'<text x="102" y="{y+742+row*30}" font-family="system-ui,sans-serif" font-size="16" fill="{accent}">{escape(note[:112])}</text>')
                row += 1
    parts.append('</svg>')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts) + "\n")
