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


def _candidate_href(candidate: dict[str, Any], prompt_id: str, output: Path, base_path: Path) -> str:
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
    return quote(href, safe="/:")


def _render_journey_keepsake_svg(
    manifest: dict[str, Any], contract: dict[str, Any], prompt_map: dict[str, Any], output: Path, base_path: Path
) -> None:
    prompt_ids = list(prompt_map)
    width = 1200
    section_height = 1420
    height = 80 + section_height * len(prompt_ids)
    paper = "#EEE7D9"
    ticket = "#F8F3E8"
    ink = "#232721"
    accent = "#49656A"
    muted = "#74786E"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" data-presentation-style="journey-keepsake">',
        f'<rect width="{width}" height="{height}" fill="{paper}"/>',
        '<defs>',
    ]
    for index in range(len(prompt_ids)):
        y = 60 + index * section_height
        parts.append(f'<clipPath id="keepsake-image-{index}"><rect x="338" y="{y+92}" width="742" height="900" rx="8"/></clipPath>')
    parts.append('</defs>')
    entries = contract.get("entries", [])
    for prompt_index, prompt_id in enumerate(prompt_ids):
        prompt = prompt_map[prompt_id]
        candidate = prompt["candidate_output"]
        encoded_href = _candidate_href(candidate, prompt_id, output, base_path)
        y = 60 + prompt_index * section_height
        prompt_entries = [entry for entry in entries if entry.get("prompt_id") == prompt_id]
        metadata: list[str] = []
        captions: list[str] = []
        notes: list[str] = []
        for entry in prompt_entries:
            caption = str(entry.get("caption", "")).strip()
            if caption:
                captions.append(caption)
            details = " · ".join(
                str(entry[field]).strip()
                for field in ("location", "date", "collection", "catalogue_id")
                if str(entry.get(field, "")).strip()
            )
            if details:
                metadata.append(details)
            note = str(entry.get("source_note", "")).strip()
            if note:
                notes.append(note)
        display_name = escape(str(contract.get("display_name", manifest.get("system", ""))))
        title = escape((captions[0] if captions else display_name)[:42])
        parts.extend([
            f'<rect x="70" y="{y}" width="1060" height="1320" rx="18" fill="{ticket}" stroke="#C9C0AE" stroke-width="2"/>',
            f'<rect x="70" y="{y}" width="232" height="1320" rx="18" fill="#DDE4DF"/>',
            f'<line x1="302" y1="{y+30}" x2="302" y2="{y+1290}" stroke="#9EAA9F" stroke-width="2" stroke-dasharray="3 13"/>',
            f'<text x="118" y="{y+1030}" font-family="system-ui,sans-serif" font-size="15" letter-spacing="3" fill="{accent}" transform="rotate(-90 118 {y+1030})">SCENE CARD STUDIO · JOURNEY KEEPSAKE</text>',
            f'<text x="224" y="{y+1240}" text-anchor="start" font-family="ui-monospace,monospace" font-size="13" fill="{muted}" transform="rotate(-90 224 {y+1240})">{escape(prompt_id.upper())} · {escape(candidate["sha256"][:12])}</text>',
            f'<image href="{encoded_href}" x="338" y="{y+92}" width="742" height="900" preserveAspectRatio="xMidYMid slice" clip-path="url(#keepsake-image-{prompt_index})"/>',
            f'<rect x="338" y="{y+92}" width="742" height="900" rx="8" fill="none" stroke="#D2C8B6"/>',
            f'<text x="338" y="{y+1054}" font-family="system-ui,sans-serif" font-size="15" letter-spacing="3" fill="{accent}">{display_name.upper()}</text>',
            f'<text x="338" y="{y+1112}" font-family="system-ui,sans-serif" font-size="40" fill="{ink}">{title}</text>',
        ])
        if metadata:
            parts.append(f'<text x="338" y="{y+1160}" font-family="system-ui,sans-serif" font-size="18" fill="{muted}">{escape(metadata[0][:84])}</text>')
        if notes:
            parts.append(f'<text x="338" y="{y+1204}" font-family="system-ui,sans-serif" font-size="17" fill="{ink}">{escape(notes[0][:96])}</text>')
        parts.extend([
            f'<line x1="338" y1="{y+1254}" x2="1080" y2="{y+1254}" stroke="#B6AD9D"/>',
            f'<circle cx="1006" cy="{y+1300}" r="13" fill="#9DAEAA"/>',
            f'<circle cx="1043" cy="{y+1300}" r="13" fill="#C7A987"/>',
            f'<circle cx="1080" cy="{y+1300}" r="13" fill="#737C69"/>',
        ])
    parts.append('</svg>')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts) + "\n")


def render_presentation_svg(
    manifest: dict[str, Any], output: Path, base: Path | None = None, style: str = "standard"
) -> None:
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

    if style not in {"standard", "journey-keepsake"}:
        raise ValueError(f"Unknown presentation style: {style}")
    base_path = (base or Path.cwd()).resolve()
    if style == "journey-keepsake":
        _render_journey_keepsake_svg(manifest, contract, prompt_map, output, base_path)
        return

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
    for prompt_index, prompt_id in enumerate(prompt_ids):
        prompt = prompt_map[prompt_id]
        candidate = prompt["candidate_output"]
        encoded_href = _candidate_href(candidate, prompt_id, output, base_path)
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
