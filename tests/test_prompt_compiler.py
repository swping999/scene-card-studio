import json
from hashlib import sha256
from pathlib import Path

import pytest

from moments_to_pages.cli import main
from moments_to_pages.director import recommend_systems
from moments_to_pages.model import Direction, Interpretation, Observation, SceneCard, TransformationPolicy
from moments_to_pages.privacy import build_upload_consent, validate_upload_consent
from moments_to_pages.prompt_compiler import SUPPORTED_SYSTEMS, compile_manifest
from moments_to_pages.review import bind_outputs, build_retry_manifest, review_decision


def _cards(tmp_path: Path) -> list[SceneCard]:
    cards = []
    for index, name in enumerate(("bus-stop.jpg", "diner.jpg")):
        source = tmp_path / name
        source.write_bytes(f"source-{index}".encode())
        cards.append(SceneCard(
            source=name,
            width=1500,
            height=1000,
            palette=["#1C2C42", "#C88B55"],
            brightness=.35,
            saturation=.22,
            orientation="landscape",
            caption=f"FRAME {index + 1}",
            observation=Observation(
                subjects=["person", "rainy street", "plastic sign"],
                dominant_gesture="small figure waiting beside reflected light",
                quiet_regions=["wet pavement"],
            ),
            interpretation=Interpretation(
                narrative_intent="departure after waiting",
                emotional_tone=["suspended", "quiet"],
                confidence=.8,
                method="user-directed",
            ),
            direction=Direction(
                story_role="opening" if index == 0 else "closing",
                director_note="Let the reflected light carry the movement.",
                layout_emphasis="figure within rain",
            ),
            transformation=TransformationPolicy(
                must_preserve=["person", "rainy street"],
                may_transform=["crop", "exposure"],
                must_remove=["plastic sign"],
            ),
        ))
    return cards


def _assessment(manifest: dict, manifest_hash: str, scores: dict | None = None) -> dict:
    default_scores = {name: 5 for name in manifest["review_policy"]["dimensions"]}
    return {
        "schema_version": "1.0",
        "manifest_sha256": manifest_hash,
        "reviewer": {"type": "model-assisted", "name": "test reviewer", "model": "test-model"},
        "reviewed_at": "2026-08-09T10:00:00Z",
        "review_method": "side-by-side visual inspection",
        "results": [{
            "prompt_id": prompt["id"],
            "output_sha256": (prompt.get("candidate_output") or prompt.get("reference_output"))["sha256"],
            "scores": scores or default_scores,
        } for prompt in manifest["prompts"]],
        "sequence_scores": {name: 5 for name in manifest["review_policy"]["sequence_dimensions"]},
    }


def test_four_systems_compile_with_policy_and_replaceable_profiles(tmp_path: Path):
    cards = _cards(tmp_path)
    expected = {
        "subject_fidelity", "transformation_policy", "narrative_intent", "composition", "lighting", "material",
        "spatial_relationships", "text_strategy", "exclusions", "output",
    }
    manifests = {}
    for system in SUPPORTED_SYSTEMS:
        manifest = compile_manifest(cards, system, source_root=tmp_path)
        manifests[system] = manifest
        assert manifest["compiler_version"] == "0.3.1"
        assert manifest["expression_profile"] == "source-led"
        assert set(manifest["prompts"][0]["blocks"]) == expected
        assert manifest["prompts"][0]["sources"][0]["sha256"]
        assert "MUST REMOVE — plastic sign" in manifest["prompts"][0]["compiled_prompt"]
        assert manifest["privacy"]["upload_requires_explicit_consent"] is True
    assert len(manifests["cinematic-storyboard"]["prompts"]) == 2
    assert len(manifests["minimal-editorial"]["prompts"]) == 2
    watercolor = compile_manifest(cards, "memory-atlas", source_root=tmp_path, expression_profile="watercolor-contour")
    assert "watercolor terrain" in watercolor["prompts"][0]["compiled_prompt"]
    assert "watercolor terrain" not in manifests["memory-atlas"]["prompts"][0]["compiled_prompt"]


def test_compiler_fails_closed_for_missing_source(tmp_path: Path):
    cards = _cards(tmp_path)
    (tmp_path / "bus-stop.jpg").unlink()
    with pytest.raises(FileNotFoundError):
        compile_manifest(cards, "minimal-editorial", source_root=tmp_path)


def test_review_is_bound_to_manifest_and_output_hashes(tmp_path: Path):
    output = tmp_path / "accepted.png"
    output.write_bytes(b"accepted-output")
    manifest = compile_manifest(_cards(tmp_path)[:1], "minimal-editorial", source_root=tmp_path, reference_outputs=[output.name])
    manifest_bytes = json.dumps(manifest, sort_keys=True).encode()
    manifest_hash = sha256(manifest_bytes).hexdigest()
    low_scores = {
        "subject_fidelity": 5, "narrative_alignment": 4, "composition": 3,
        "system_distinctiveness": 4, "artifact_control": 2,
    }
    assessment = _assessment(manifest, manifest_hash, low_scores)
    assessment["results"][0]["notes"] = "Remove the synthetic cable and restore the chair legs."
    retry = build_retry_manifest(manifest, assessment, manifest_sha256=manifest_hash)
    assert retry["retry_prompt_ids"] == [manifest["prompts"][0]["id"]]
    correction = retry["prompts"][0]["compiled_prompt"].split("TARGETED CORRECTION PASS", 1)[1]
    assert "composition:" in correction and "artifact_control:" in correction
    assert "subject_fidelity:" not in correction
    wrong = json.loads(json.dumps(assessment))
    wrong["results"][0]["output_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="output_sha256"):
        build_retry_manifest(manifest, wrong, manifest_sha256=manifest_hash)
    with pytest.raises(ValueError, match="manifest_sha256"):
        build_retry_manifest(manifest, assessment, manifest_sha256="f" * 64)
    assert review_decision({name: 4 for name in manifest["review_policy"]["dimensions"]}) == ("accept", [])


def test_sequence_failure_retries_every_cinematic_frame(tmp_path: Path):
    outputs = []
    for index in range(2):
        path = tmp_path / f"output-{index}.png"
        path.write_bytes(f"output-{index}".encode())
        outputs.append(path.name)
    manifest = compile_manifest(_cards(tmp_path), "cinematic-storyboard", source_root=tmp_path, reference_outputs=outputs)
    manifest_hash = "a" * 64
    assessment = _assessment(manifest, manifest_hash)
    assessment["sequence_scores"]["light_color_continuity"] = 2
    retry = build_retry_manifest(manifest, assessment, manifest_sha256=manifest_hash)
    assert retry["retry_prompt_ids"] == [item["id"] for item in manifest["prompts"]]
    assert all("sequence.light_color_continuity" in item["compiled_prompt"] for item in retry["prompts"])


def test_cli_bind_outputs_retry_and_consent(tmp_path: Path):
    cards = _cards(tmp_path)[:1]
    story = tmp_path / "story.json"
    story.write_text(json.dumps([card.to_dict() for card in cards]))
    manifest_path = tmp_path / "prompts.json"
    assert main(["compile", str(story), "--system", "cinematic-storyboard", "-o", str(manifest_path)]) == 0
    output = tmp_path / "generated.png"
    output.write_bytes(b"generated")
    bound_path = tmp_path / "render-manifest.json"
    assert main(["bind-outputs", str(manifest_path), "--result", f"cinematic-storyboard-01={output}", "-o", str(bound_path)]) == 0
    bound = json.loads(bound_path.read_text())
    manifest_hash = sha256(bound_path.read_bytes()).hexdigest()
    assessment = _assessment(bound, manifest_hash)
    assessment_path = tmp_path / "assessment.json"
    assessment_path.write_text(json.dumps(assessment))
    retry_path = tmp_path / "retry.json"
    assert main(["retry", str(bound_path), str(assessment_path), "-o", str(retry_path)]) == 0
    assert json.loads(retry_path.read_text())["retry_prompt_ids"] == []
    consent_path = tmp_path / "consent.json"
    assert main(["consent", str(manifest_path), "--provider", "example-provider", "--purpose", "art direction", "--confirm", "-o", str(consent_path)]) == 0
    consent = json.loads(consent_path.read_text())
    original = json.loads(manifest_path.read_text())
    validate_upload_consent(consent, original, sha256(manifest_path.read_bytes()).hexdigest())


def test_recommender_supports_english_and_chinese(tmp_path: Path):
    cinematic = _cards(tmp_path)
    assert recommend_systems(cinematic)[0].system == "cinematic-storyboard"

    minimal = _cards(tmp_path)
    for card, subject in zip(minimal, ("杯子", "亚麻")):
        card.observation.subjects = [subject, "材质表面"]
        card.observation.dominant_gesture = "物件处于留白中"
        card.interpretation.narrative_intent = "安静的静物研究"
        card.interpretation.emotional_tone = ["安静", "触感"]
        card.direction.director_note = "保留磨损并移除杂物。"
    assert recommend_systems(minimal)[0].system == "minimal-editorial"

    family = _cards(tmp_path)
    for card in family:
        card.interpretation.narrative_intent = "家庭照料与代际传承"
    assert recommend_systems(family)[0].system == "family-archive"

    journey = _cards(tmp_path)
    for card in journey:
        card.interpretation.narrative_intent = "旅途中的距离与离开"
    assert recommend_systems(journey)[0].system in {"memory-atlas", "cinematic-storyboard"}


def test_published_example_reviews_match_their_manifests():
    root = Path(__file__).resolve().parents[1]
    pairs = [
        (root / "examples/prompt-manifest.json", root / "examples/accepted-review.json"),
        (root / "examples/cases/family-archive/prompt-manifest.json", root / "examples/cases/family-archive/accepted-review.json"),
        (root / "examples/cases/cinematic-storyboard/prompt-manifest.json", root / "examples/cases/cinematic-storyboard/accepted-review.json"),
        (root / "examples/cases/minimal-editorial/prompt-manifest.json", root / "examples/cases/minimal-editorial/accepted-review.json"),
    ]
    for manifest_path, review_path in pairs:
        manifest = json.loads(manifest_path.read_text())
        assessment = json.loads(review_path.read_text())
        retry = build_retry_manifest(
            manifest,
            assessment,
            manifest_sha256=sha256(manifest_path.read_bytes()).hexdigest(),
        )
        assert retry["retry_prompt_ids"] == []
