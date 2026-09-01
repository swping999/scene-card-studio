from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from math import gcd
from pathlib import Path
from typing import Any

from .prompt_compiler import REVIEW_POLICY

CORRECTIONS = {
    "subject_fidelity": "Restore the exact source identity, count, proportions, pose, action, architecture, and defining material details. Do not redesign the subject.",
    "narrative_alignment": "Strengthen the stated narrative intent, emotional tone, story role, and director note without adding new story facts.",
    "composition": "Rebuild the visual hierarchy, crop, depth, and negative space while preserving the source subject and scene logic.",
    "system_distinctiveness": "Apply the selected Narrative System mechanism and expression profile; remove generic beauty-treatment choices.",
    "artifact_control": "Remove distorted anatomy, broken geometry, unwanted text, collage seams, synthetic clutter, and invented metadata.",
}

SEQUENCE_CORRECTIONS = {
    "subject_continuity": "Restore recurring people, clothing, objects, locations, and identity-bearing details consistently across every frame.",
    "light_color_continuity": "Unify motivated light direction, exposure progression, and palette across the sequence without flattening individual scenes.",
    "rhythm": "Vary shot scale and density to restore intentional pacing and a readable pause; avoid repetitive framing.",
    "narrative_arc": "Clarify the supplied opening, development, pause, and closing roles without inventing events or chronology.",
}


def file_sha256(path: Path) -> str:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Output file does not exist: {path}")
    return sha256(path.read_bytes()).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _image_record(path: Path, display_path: str) -> dict[str, Any]:
    try:
        from PIL import Image, UnidentifiedImageError
    except ImportError as exc:
        raise RuntimeError("Output binding requires Pillow: pip install 'scene-card-studio[images]'") from exc
    try:
        with Image.open(path) as opened:
            opened.verify()
        with Image.open(path) as opened:
            width, height = opened.size
            mime = Image.MIME.get(opened.format or "")
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(f"Candidate output is not a decodable image: {path}") from exc
    if not mime:
        raise ValueError(f"Candidate output has an unsupported image format: {path}")
    divisor = gcd(width, height)
    return {
        "path": display_path,
        "sha256": file_sha256(path),
        "mime_type": mime,
        "width": width,
        "height": height,
        "aspect_ratio": f"{width // divisor}:{height // divisor}",
    }


def _validate_output_contract(prompt: dict[str, Any], record: dict[str, Any]) -> None:
    contract = prompt.get("output_contract")
    if not isinstance(contract, dict):
        raise ValueError(f"Prompt {prompt.get('id')} has no structured output_contract")
    mismatches = [
        field for field in ("mime_type", "width", "height", "aspect_ratio")
        if record.get(field) != contract.get(field)
    ]
    if mismatches:
        details = ", ".join(f"{field}={record.get(field)!r} (expected {contract.get(field)!r})" for field in mismatches)
        raise ValueError(f"Candidate output violates {prompt.get('id')} output_contract: {details}")


def bind_outputs(
    manifest: dict[str, Any],
    bindings: dict[str, str],
    *,
    manifest_sha256: str,
    base: Path | None = None,
) -> dict[str, Any]:
    output = deepcopy(manifest)
    prompts = {item["id"]: item for item in output.get("prompts", [])}
    unknown = set(bindings) - set(prompts)
    if unknown:
        raise ValueError(f"Unknown prompt ids: {', '.join(sorted(unknown))}")
    if set(prompts) - set(bindings):
        missing = set(prompts) - set(bindings)
        raise ValueError(f"Missing output bindings for: {', '.join(sorted(missing))}")
    for prompt_id, value in bindings.items():
        supplied = Path(value).expanduser()
        resolved = supplied if supplied.is_absolute() else ((base or Path.cwd()) / supplied)
        record = _image_record(resolved, value)
        _validate_output_contract(prompts[prompt_id], record)
        prompts[prompt_id]["candidate_output"] = record
    output["artifact_type"] = "render-manifest"
    output["render_manifest_version"] = "1.0"
    output["parent_manifest_sha256"] = manifest_sha256
    output["bound_at"] = _now()
    return output


def _score_decision(scores: dict[str, int], dimensions: dict[str, str]) -> tuple[str, list[str]]:
    if not isinstance(scores, dict):
        raise ValueError("Review scores must be an object")
    unknown = sorted(set(scores) - set(dimensions))
    if unknown:
        raise ValueError(f"Unknown review scores: {', '.join(unknown)}")
    missing = [name for name in dimensions if name not in scores]
    if missing:
        raise ValueError(f"Missing review scores: {', '.join(missing)}")
    invalid = [name for name, value in scores.items() if name in dimensions and (not isinstance(value, int) or not 1 <= value <= 5)]
    if invalid:
        raise ValueError(f"Review scores must be integers from 1 to 5: {', '.join(invalid)}")
    threshold = REVIEW_POLICY["accept_threshold"]
    failed = [name for name in dimensions if scores[name] < threshold]
    return ("accept" if not failed else "retry", failed)


def review_decision(scores: dict[str, int]) -> tuple[str, list[str]]:
    return _score_decision(scores, REVIEW_POLICY["dimensions"])


def sequence_review_decision(scores: dict[str, int]) -> tuple[str, list[str]]:
    return _score_decision(scores, REVIEW_POLICY["sequence_dimensions"])


def build_review_template(
    manifest: dict[str, Any],
    *,
    manifest_sha256: str,
    reviewer_type: str,
    reviewer_name: str,
    reviewer_model: str,
    review_method: str,
) -> dict[str, Any]:
    if manifest.get("artifact_type") != "render-manifest":
        raise ValueError("Review template requires a Render Manifest produced by bind-outputs")
    reviewer = {
        "type": reviewer_type.strip(),
        "name": reviewer_name.strip(),
        "model": reviewer_model.strip(),
    }
    for field, value in reviewer.items():
        if not value:
            raise ValueError(f"reviewer.{field} is required")
    if not review_method.strip():
        raise ValueError("review_method is required")
    results = []
    for prompt in manifest.get("prompts", []):
        results.append({
            "prompt_id": prompt.get("id"),
            "output_sha256": _expected_output_hash(prompt),
            "scores": {name: None for name in REVIEW_POLICY["dimensions"]},
            "notes": "",
        })
    if not results:
        raise ValueError("Render Manifest contains no prompts")
    template: dict[str, Any] = {
        "artifact_type": "aesthetic-review-template",
        "schema_version": "1.0",
        "manifest_sha256": manifest_sha256,
        "reviewer": reviewer,
        "template_created_at": _now(),
        "reviewed_at": None,
        "review_method": review_method.strip(),
        "results": results,
    }
    if manifest.get("sequence_review_required") and len(results) > 1:
        template["sequence_scores"] = {name: None for name in REVIEW_POLICY["sequence_dimensions"]}
    return template


def build_review_record(
    manifest: dict[str, Any],
    assessment: dict[str, Any],
    *,
    manifest_sha256: str,
) -> dict[str, Any]:
    normalized = deepcopy(assessment)
    if not isinstance(normalized.get("reviewed_at"), str) or not normalized["reviewed_at"].strip():
        normalized["reviewed_at"] = _now()
    _validate_assessment_metadata(normalized, manifest, manifest_sha256)
    prompts = {item.get("id"): item for item in manifest.get("prompts", [])}
    result_items = normalized.get("results")
    if not isinstance(result_items, list):
        raise ValueError("Assessment results must be a list")
    result_ids = [item.get("prompt_id") for item in result_items if isinstance(item, dict)]
    if len(result_ids) != len(result_items):
        raise ValueError("Every assessment result must be an object with prompt_id")
    if len(result_ids) != len(set(result_ids)):
        raise ValueError("Assessment contains duplicate prompt ids")
    unknown = sorted(set(result_ids) - set(prompts))
    if unknown:
        raise ValueError(f"Assessment contains unknown prompt ids: {', '.join(unknown)}")
    missing = sorted(set(prompts) - set(result_ids))
    if missing:
        raise ValueError(f"Missing assessment for prompt ids: {', '.join(missing)}")

    output_results = []
    failed_prompt_ids: list[str] = []
    for result in result_items:
        prompt_id = result["prompt_id"]
        if result.get("output_sha256") != _expected_output_hash(prompts[prompt_id]):
            raise ValueError(f"Assessment output_sha256 does not match prompt {prompt_id}")
        decision, failed = review_decision(result.get("scores", {}))
        reviewed = deepcopy(result)
        reviewed["decision"] = decision
        reviewed["failed_dimensions"] = failed
        output_results.append(reviewed)
        if failed:
            failed_prompt_ids.append(prompt_id)

    sequence_failed: list[str] = []
    if manifest.get("sequence_review_required") and len(prompts) > 1:
        _, sequence_failed = sequence_review_decision(assessment.get("sequence_scores", {}))

    record = normalized
    record["artifact_type"] = "aesthetic-review"
    record["review_version"] = "1.0"
    record["results"] = output_results
    record["decision"] = "retry" if failed_prompt_ids or sequence_failed else "accept"
    record["failed_prompt_ids"] = failed_prompt_ids
    record["sequence_decision"] = "retry" if sequence_failed else "accept"
    record["sequence_failed_dimensions"] = sequence_failed
    record["retry_prompt_ids"] = list(prompts) if sequence_failed else failed_prompt_ids
    return record


def _validate_assessment_metadata(assessment: dict[str, Any], manifest: dict[str, Any], expected_manifest_sha256: str) -> None:
    if manifest.get("artifact_type") != "render-manifest":
        raise ValueError("Formal review requires a Render Manifest produced by bind-outputs")
    if assessment.get("manifest_sha256") != expected_manifest_sha256:
        raise ValueError("Assessment manifest_sha256 does not match the reviewed manifest")
    reviewer = assessment.get("reviewer")
    if not isinstance(reviewer, dict):
        raise ValueError("Assessment reviewer metadata is required")
    for field in ("type", "name", "model"):
        if not isinstance(reviewer.get(field), str) or not reviewer[field].strip():
            raise ValueError(f"Assessment reviewer.{field} is required")
    method = assessment.get("review_method")
    if not isinstance(method, str) or not method.strip():
        raise ValueError("Assessment review_method is required")
    reviewed_at = assessment.get("reviewed_at")
    if not isinstance(reviewed_at, str):
        raise ValueError("Assessment reviewed_at is required")
    try:
        reviewed = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Assessment reviewed_at must be ISO 8601") from exc
    if reviewed.tzinfo is None or reviewed.utcoffset() is None:
        raise ValueError("Assessment reviewed_at must include a timezone")
    bound_at = manifest.get("bound_at")
    if isinstance(bound_at, str):
        try:
            bound = datetime.fromisoformat(bound_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("Render Manifest bound_at must be ISO 8601") from exc
        if bound.tzinfo is None or bound.utcoffset() is None:
            raise ValueError("Render Manifest bound_at must include a timezone")
        if reviewed < bound:
            raise ValueError("Assessment reviewed_at predates the bound Render Manifest")
    if reviewed > datetime.now(timezone.utc):
        raise ValueError("Assessment reviewed_at is in the future")


def _expected_output_hash(prompt: dict[str, Any]) -> str:
    record = prompt.get("candidate_output")
    if not isinstance(record, dict) or not record.get("sha256"):
        raise ValueError(f"Prompt {prompt.get('id')} has no candidate_output; run bind-outputs before formal review")
    _validate_output_contract(prompt, record)
    return str(record["sha256"])


def build_retry_manifest(
    manifest: dict[str, Any],
    assessment: dict[str, Any],
    *,
    manifest_sha256: str,
    assessment_sha256: str,
) -> dict[str, Any]:
    _validate_assessment_metadata(assessment, manifest, manifest_sha256)
    original = {item["id"]: item for item in manifest.get("prompts", [])}
    result_items = assessment.get("results", [])
    if not isinstance(result_items, list):
        raise ValueError("Assessment results must be a list")
    results = {item["prompt_id"]: item for item in result_items}
    if len(results) != len(result_items):
        raise ValueError("Assessment contains duplicate prompt ids")
    if set(results) - set(original):
        unknown = ", ".join(sorted(set(results) - set(original)))
        raise ValueError(f"Assessment contains unknown prompt ids: {unknown}")

    sequence_failed: list[str] = []
    if manifest.get("sequence_review_required") and len(original) > 1:
        _, sequence_failed = sequence_review_decision(assessment.get("sequence_scores", {}))

    output = deepcopy(manifest)
    output["artifact_type"] = "retry-manifest"
    output["retry_manifest_version"] = "1.0"
    output["parent_render_manifest_sha256"] = manifest_sha256
    output["parent_prompt_manifest_sha256"] = manifest.get("parent_manifest_sha256")
    output["failed_review_sha256"] = assessment_sha256
    output["generated_at"] = _now()
    output.pop("bound_at", None)
    output.pop("render_manifest_version", None)
    output["retry_iteration"] = int(manifest.get("retry_iteration", 0)) + 1
    retry_prompts: list[str] = []
    decisions = []
    for item in output.get("prompts", []):
        reviewed_item = original[item["id"]]
        result = results.get(item["id"])
        if result is None:
            raise ValueError(f"Missing assessment for prompt id: {item['id']}")
        if result.get("output_sha256") != _expected_output_hash(reviewed_item):
            raise ValueError(f"Assessment output_sha256 does not match prompt {item['id']}")
        item.pop("candidate_output", None)
        decision, failed = review_decision(result.get("scores", {}))
        all_failed = list(failed)
        if sequence_failed:
            all_failed.extend(f"sequence.{name}" for name in sequence_failed)
        decisions.append({"prompt_id": item["id"], "decision": "retry" if all_failed else decision, "failed_dimensions": all_failed})
        if all_failed:
            notes = str(result.get("notes", "")).strip()
            correction_lines = [f"- {name}: {CORRECTIONS[name]}" for name in failed]
            correction_lines.extend(f"- sequence.{name}: {SEQUENCE_CORRECTIONS[name]}" for name in sequence_failed)
            if notes:
                correction_lines.append(f"- Reviewer note: {notes}")
            item["compiled_prompt"] += (
                "\n\nTARGETED CORRECTION PASS\n"
                "Keep every successful decision unchanged. Correct only the failed dimensions below.\n"
                + "\n".join(correction_lines)
            )
            retry_prompts.append(item["id"])
    output["review_binding"] = {
        "reviewed_manifest_sha256": manifest_sha256,
        "reviewer": assessment["reviewer"],
        "reviewed_at": assessment["reviewed_at"],
        "review_method": assessment["review_method"],
        "assessment_sha256": assessment_sha256,
    }
    output["review_decisions"] = decisions
    output["sequence_review"] = {"decision": "retry" if sequence_failed else "accept", "failed_dimensions": sequence_failed}
    output["retry_prompt_ids"] = retry_prompts
    return output
