import json
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

import pytest
from PIL import Image

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
        "reviewed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "review_method": "side-by-side visual inspection",
        "results": [{
            "prompt_id": prompt["id"],
            "output_sha256": prompt["candidate_output"]["sha256"],
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
        assert manifest["compiler_version"] == "0.3.2"
        assert manifest["schema_version"] == "1.2"
        assert manifest["expression_profile"] == "source-led"
        assert set(manifest["prompts"][0]["blocks"]) == expected
        assert manifest["prompts"][0]["sources"][0]["sha256"]
        assert set(manifest["prompts"][0]["output_contract"]) == {"mime_type", "width", "height", "aspect_ratio"}
        assert "MUST REMOVE — plastic sign" in manifest["prompts"][0]["compiled_prompt"]
        assert manifest["privacy"]["upload_requires_explicit_consent"] is True
    assert len(manifests["cinematic-storyboard"]["prompts"]) == 2
    assert len(manifests["minimal-editorial"]["prompts"]) == 2
    watercolor = compile_manifest(cards, "memory-atlas", source_root=tmp_path, expression_profile="watercolor-contour")
    assert "watercolor terrain" in watercolor["prompts"][0]["compiled_prompt"]
    assert "watercolor terrain" not in manifests["memory-atlas"]["prompts"][0]["compiled_prompt"]
    widescreen = compile_manifest(cards[:1], "cinematic-storyboard", source_root=tmp_path, aspect_ratio="16:9")
    contract = widescreen["prompts"][0]["output_contract"]
    assert contract["width"] * 9 == contract["height"] * 16


def test_compiler_fails_closed_for_missing_source(tmp_path: Path):
    cards = _cards(tmp_path)
    (tmp_path / "bus-stop.jpg").unlink()
    with pytest.raises(FileNotFoundError):
        compile_manifest(cards, "minimal-editorial", source_root=tmp_path)


def test_review_is_bound_to_manifest_and_output_hashes(tmp_path: Path):
    output = tmp_path / "accepted.png"
    Image.new("RGB", (1536, 1024), "navy").save(output)
    prompt_manifest = compile_manifest(_cards(tmp_path)[:1], "minimal-editorial", source_root=tmp_path)
    with pytest.raises(ValueError, match="Render Manifest"):
        build_retry_manifest(prompt_manifest, {}, manifest_sha256="0" * 64, assessment_sha256="1" * 64)
    manifest = bind_outputs(prompt_manifest, {"minimal-editorial-01": str(output)}, manifest_sha256="a" * 64)
    manifest_hash = sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
    low_scores = {
        "subject_fidelity": 5, "narrative_alignment": 4, "composition": 3,
        "system_distinctiveness": 4, "artifact_control": 2,
    }
    assessment = _assessment(manifest, manifest_hash, low_scores)
    assessment["results"][0]["notes"] = "Remove the synthetic cable and restore the chair legs."
    retry = build_retry_manifest(manifest, assessment, manifest_sha256=manifest_hash, assessment_sha256="b" * 64)
    assert retry["retry_prompt_ids"] == [manifest["prompts"][0]["id"]]
    correction = retry["prompts"][0]["compiled_prompt"].split("TARGETED CORRECTION PASS", 1)[1]
    assert "composition:" in correction and "artifact_control:" in correction
    assert "subject_fidelity:" not in correction
    wrong = json.loads(json.dumps(assessment))
    wrong["results"][0]["output_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="output_sha256"):
        build_retry_manifest(manifest, wrong, manifest_sha256=manifest_hash, assessment_sha256="b" * 64)
    with pytest.raises(ValueError, match="manifest_sha256"):
        build_retry_manifest(manifest, assessment, manifest_sha256="f" * 64, assessment_sha256="b" * 64)
    assert review_decision({name: 4 for name in manifest["review_policy"]["dimensions"]}) == ("accept", [])


def test_reference_output_cannot_substitute_for_candidate_output(tmp_path: Path):
    benchmark = tmp_path / "benchmark.png"
    Image.new("RGB", (1536, 1024), "navy").save(benchmark)
    manifest = compile_manifest(
        _cards(tmp_path)[:1],
        "minimal-editorial",
        source_root=tmp_path,
        reference_outputs=[benchmark.name],
    )
    manifest["artifact_type"] = "render-manifest"
    manifest["bound_at"] = "2026-08-09T00:00:00Z"
    assessment = {
        "manifest_sha256": "a" * 64,
        "reviewer": {"type": "human", "name": "test", "model": "visual"},
        "review_method": "comparison",
        "reviewed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "results": [{
            "prompt_id": "minimal-editorial-01",
            "output_sha256": manifest["prompts"][0]["reference_output"]["sha256"],
            "scores": {name: 5 for name in manifest["review_policy"]["dimensions"]},
        }],
    }
    with pytest.raises(ValueError, match="no candidate_output"):
        build_retry_manifest(manifest, assessment, manifest_sha256="a" * 64, assessment_sha256="b" * 64)


def test_review_timestamp_requires_timezone(tmp_path: Path):
    output = tmp_path / "candidate.png"
    Image.new("RGB", (1536, 1024), "navy").save(output)
    prompt_manifest = compile_manifest(_cards(tmp_path)[:1], "minimal-editorial", source_root=tmp_path)
    manifest = bind_outputs(
        prompt_manifest,
        {"minimal-editorial-01": str(output)},
        manifest_sha256="a" * 64,
    )
    manifest_hash = sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
    assessment = _assessment(manifest, manifest_hash)
    assessment["reviewed_at"] = "2026-08-09T12:00:00"
    with pytest.raises(ValueError, match="include a timezone"):
        build_retry_manifest(manifest, assessment, manifest_sha256=manifest_hash, assessment_sha256="b" * 64)


def test_sequence_failure_retries_every_cinematic_frame(tmp_path: Path):
    outputs = []
    for index in range(2):
        path = tmp_path / f"output-{index}.png"
        Image.new("RGB", (1536, 1024), (20 + index, 30, 40)).save(path)
        outputs.append(str(path))
    prompt_manifest = compile_manifest(_cards(tmp_path), "cinematic-storyboard", source_root=tmp_path)
    manifest = bind_outputs(
        prompt_manifest,
        {f"cinematic-storyboard-{index + 1:02d}": path for index, path in enumerate(outputs)},
        manifest_sha256="c" * 64,
    )
    manifest_hash = "a" * 64
    assessment = _assessment(manifest, manifest_hash)
    assessment["sequence_scores"]["light_color_continuity"] = 2
    retry = build_retry_manifest(manifest, assessment, manifest_sha256=manifest_hash, assessment_sha256="d" * 64)
    assert retry["retry_prompt_ids"] == [item["id"] for item in manifest["prompts"]]
    assert all("sequence.light_color_continuity" in item["compiled_prompt"] for item in retry["prompts"])
    assert retry["parent_render_manifest_sha256"] == manifest_hash
    assert retry["failed_review_sha256"] == "d" * 64
    assert all("candidate_output" not in item for item in retry["prompts"])


def test_cli_bind_outputs_retry_and_consent(tmp_path: Path):
    cards = _cards(tmp_path)[:1]
    story = tmp_path / "story.json"
    story.write_text(json.dumps([card.to_dict() for card in cards]))
    manifest_path = tmp_path / "prompts.json"
    assert main(["compile", str(story), "--system", "cinematic-storyboard", "-o", str(manifest_path)]) == 0
    output = tmp_path / "generated.png"
    Image.new("RGB", (1536, 1024), "green").save(output)
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


def test_output_contract_rejects_wrong_dimensions(tmp_path: Path):
    prompt_manifest = compile_manifest(_cards(tmp_path)[:1], "minimal-editorial", source_root=tmp_path)
    wrong = tmp_path / "wrong.png"
    Image.new("RGB", (1024, 1024), "red").save(wrong)
    with pytest.raises(ValueError, match="output_contract"):
        bind_outputs(prompt_manifest, {"minimal-editorial-01": str(wrong)}, manifest_sha256="e" * 64)


def test_published_example_reviews_match_their_render_manifests():
    root = Path(__file__).resolve().parents[1]
    pairs = [
        (root / "examples/prompt-manifest.json", root / "examples/render-manifest.json", root / "examples/accepted-review.json"),
        (root / "examples/cases/family-archive/prompt-manifest.json", root / "examples/cases/family-archive/render-manifest.json", root / "examples/cases/family-archive/accepted-review.json"),
        (root / "examples/cases/cinematic-storyboard/retry-example/retry-manifest.json", root / "examples/cases/cinematic-storyboard/retry-example/post-retry-render-manifest.json", root / "examples/cases/cinematic-storyboard/accepted-review.json"),
        (root / "examples/cases/minimal-editorial/prompt-manifest.json", root / "examples/cases/minimal-editorial/render-manifest.json", root / "examples/cases/minimal-editorial/accepted-review.json"),
    ]
    for parent_path, manifest_path, review_path in pairs:
        manifest = json.loads(manifest_path.read_text())
        assert manifest["parent_manifest_sha256"] == sha256(parent_path.read_bytes()).hexdigest()
        assessment = json.loads(review_path.read_text())
        retry = build_retry_manifest(
            manifest,
            assessment,
            manifest_sha256=sha256(manifest_path.read_bytes()).hexdigest(),
            assessment_sha256=sha256(review_path.read_bytes()).hexdigest(),
        )
        assert retry["retry_prompt_ids"] == []


def test_published_retry_example_is_a_complete_hash_chain():
    root = Path(__file__).resolve().parents[1] / "examples/cases/cinematic-storyboard"
    prompt_path = root / "prompt-manifest.json"
    failed_render_path = root / "retry-example/failed-render-manifest.json"
    failed_review_path = root / "retry-example/failed-review.json"
    retry_path = root / "retry-example/retry-manifest.json"
    post_render_path = root / "retry-example/post-retry-render-manifest.json"
    accepted_path = root / "accepted-review.json"
    digest = lambda path: sha256(path.read_bytes()).hexdigest()
    failed_render = json.loads(failed_render_path.read_text())
    failed_review = json.loads(failed_review_path.read_text())
    retry = json.loads(retry_path.read_text())
    post_render = json.loads(post_render_path.read_text())
    accepted = json.loads(accepted_path.read_text())
    assert failed_render["parent_manifest_sha256"] == digest(prompt_path)
    assert failed_review["manifest_sha256"] == digest(failed_render_path)
    assert retry["parent_render_manifest_sha256"] == digest(failed_render_path)
    assert retry["failed_review_sha256"] == digest(failed_review_path)
    assert post_render["parent_manifest_sha256"] == digest(retry_path)
    assert accepted["manifest_sha256"] == digest(post_render_path)
    times = [failed_render["bound_at"], failed_review["reviewed_at"], retry["generated_at"], post_render["bound_at"], accepted["reviewed_at"]]
    parsed = [datetime.fromisoformat(value.replace("Z", "+00:00")) for value in times]
    assert parsed == sorted(parsed)
