from __future__ import annotations

from copy import deepcopy
from typing import Any

from .prompt_compiler import REVIEW_POLICY


CORRECTIONS = {
    "subject_fidelity": "Restore the exact source identity, count, proportions, pose, action, architecture, and defining material details. Do not redesign the subject.",
    "narrative_alignment": "Strengthen the stated narrative intent, emotional tone, story role, and director note without adding new story facts.",
    "composition": "Rebuild the visual hierarchy, crop, depth, and negative space while preserving the source subject and scene logic.",
    "system_distinctiveness": "Apply the selected Narrative System's specific spatial, material, and lighting mechanism; remove generic beauty-treatment choices.",
    "artifact_control": "Remove distorted anatomy, broken geometry, unwanted text, collage seams, synthetic clutter, and invented metadata.",
}


def review_decision(scores: dict[str, int]) -> tuple[str, list[str]]:
    dimensions = REVIEW_POLICY["dimensions"]
    missing = [name for name in dimensions if name not in scores]
    if missing:
        raise ValueError(f"Missing review scores: {', '.join(missing)}")
    invalid = [name for name, value in scores.items() if name in dimensions and (not isinstance(value, int) or not 1 <= value <= 5)]
    if invalid:
        raise ValueError(f"Review scores must be integers from 1 to 5: {', '.join(invalid)}")
    threshold = REVIEW_POLICY["accept_threshold"]
    failed = [name for name in dimensions if scores[name] < threshold]
    return ("accept" if not failed else "retry", failed)


def build_retry_manifest(manifest: dict[str, Any], assessment: dict[str, Any]) -> dict[str, Any]:
    original = {item["id"]: item for item in manifest.get("prompts", [])}
    results = {item["prompt_id"]: item for item in assessment.get("results", [])}
    if set(results) - set(original):
        unknown = ", ".join(sorted(set(results) - set(original)))
        raise ValueError(f"Assessment contains unknown prompt ids: {unknown}")

    output = deepcopy(manifest)
    output["retry_iteration"] = int(manifest.get("retry_iteration", 0)) + 1
    retry_prompts = []
    decisions = []
    for item in output.get("prompts", []):
        result = results.get(item["id"])
        if result is None:
            raise ValueError(f"Missing assessment for prompt id: {item['id']}")
        decision, failed = review_decision(result.get("scores", {}))
        decisions.append({"prompt_id": item["id"], "decision": decision, "failed_dimensions": failed})
        if decision == "retry":
            notes = str(result.get("notes", "")).strip()
            correction_lines = [f"- {name}: {CORRECTIONS[name]}" for name in failed]
            if notes:
                correction_lines.append(f"- Reviewer note: {notes}")
            item["compiled_prompt"] += (
                "\n\nTARGETED CORRECTION PASS\n"
                "Keep every successful decision unchanged. Correct only the failed dimensions below.\n"
                + "\n".join(correction_lines)
            )
            retry_prompts.append(item["id"])
    output["review_decisions"] = decisions
    output["retry_prompt_ids"] = retry_prompts
    return output
