#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from hashlib import sha256
from pathlib import Path

GALLERY = Path(__file__).resolve().parent
PROJECT_ROOT = GALLERY.parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from moments_to_pages.analyze import analyze_image
from moments_to_pages.model import (  # noqa: E402
    Direction,
    Interpretation,
    Observation,
    TransformationPolicy,
)
from moments_to_pages.prompt_compiler import compile_manifest  # noqa: E402


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def build_payloads() -> dict[Path, bytes]:
    records = json.loads((GALLERY / "case-records.json").read_text())
    payloads: dict[Path, bytes] = {}
    index_cases = []
    for case in records["cases"]:
        case_id = case["case_id"]
        evidence_dir = GALLERY / "evidence" / case_id
        before = (GALLERY / case["before"]).resolve()
        after = (GALLERY / case["after"]).resolve()
        card = analyze_image(before)
        semantic = case["scene_card"]
        card.caption = case["display_name"].upper()
        card.observation = Observation(**semantic["observation"])
        card.interpretation = Interpretation(**semantic["interpretation"])
        card.direction = Direction(**semantic["direction"])
        card.transformation = TransformationPolicy(**semantic["transformation"])
        card.source = Path(os.path.relpath(before, evidence_dir)).as_posix()
        card.validate()

        story = [card.to_dict()]
        story_path = evidence_dir / "story.json"
        story_bytes = _json_bytes(story)
        payloads[story_path] = story_bytes
        manifest = compile_manifest(
            [card],
            case["system"],
            expression_profile=case["expression_profile"],
            source_root=evidence_dir,
            story_path="story.json",
            reference_outputs=[Path(os.path.relpath(after, evidence_dir)).as_posix()],
        )
        manifest_path = evidence_dir / "prompt-manifest.json"
        manifest_bytes = _json_bytes(manifest)
        payloads[manifest_path] = manifest_bytes
        index_cases.append({
            "case_id": case_id,
            "display_name": case["display_name"],
            "system": case["system"],
            "expression_profile": case["expression_profile"],
            "story": f"{case_id}/story.json",
            "story_sha256": sha256(story_bytes).hexdigest(),
            "prompt_manifest": f"{case_id}/prompt-manifest.json",
            "prompt_manifest_sha256": sha256(manifest_bytes).hexdigest(),
            "reference_output": f"../{case['after']}",
        })
    payloads[GALLERY / "evidence" / "index.json"] = _json_bytes({
        "schema_version": "1.0",
        "source_record": "../case-records.json",
        "purpose": "Recompilable single-photo Scene Cards and Prompt Manifests for every published gallery case.",
        "cases": index_cases,
    })
    return payloads


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if committed evidence differs from regenerated output")
    args = parser.parse_args()
    if not args.check:
        records = json.loads((GALLERY / "case-records.json").read_text())
        for case in records["cases"]:
            (GALLERY / "evidence" / case["case_id"]).mkdir(parents=True, exist_ok=True)
    payloads = build_payloads()
    changed = []
    for path, content in payloads.items():
        if path.exists() and path.read_bytes() == content:
            continue
        changed.append(path.relative_to(PROJECT_ROOT).as_posix())
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if changed:
        print(("Evidence is out of date:\n" if args.check else "Updated gallery evidence:\n") + "\n".join(changed))
        return 1 if args.check else 0
    print("Gallery evidence is reproducible and up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
