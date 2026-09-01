from __future__ import annotations

import json
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

import pytest
from PIL import Image

from moments_to_pages.cli import main
from moments_to_pages.director import recommend_systems
from moments_to_pages.expression_profiles import expression_profile_names
from moments_to_pages.model import (
    Direction,
    Interpretation,
    Observation,
    SceneCard,
    TransformationPolicy,
)
from moments_to_pages.privacy import build_upload_consent, validate_upload_consent
from moments_to_pages.prompt_compiler import SUPPORTED_SYSTEMS, compile_manifest
from moments_to_pages.review import (
    bind_outputs,
    build_retry_manifest,
    build_review_record,
    build_review_template,
    review_decision,
)


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


def test_all_systems_compile_with_policy_profiles_and_presentation_contract(tmp_path: Path):
    cards = _cards(tmp_path)
    expected = {
        "subject_fidelity", "transformation_policy", "narrative_intent", "composition", "lighting", "material",
        "spatial_relationships", "text_strategy", "exclusions", "output",
    }
    manifests = {}
    for system in SUPPORTED_SYSTEMS:
        manifest = compile_manifest(cards, system, source_root=tmp_path)
        manifests[system] = manifest
        assert manifest["compiler_version"] == "0.5.0"
        assert manifest["schema_version"] == "1.5"
        assert manifest["source_mode"] == (
            "multi-photo-per-source"
            if system in {"cinematic-storyboard", "minimal-editorial", "editorial-sequence", "field-log", "museum-catalogue", "street-reportage", "fashion-editorial"}
            else "multi-photo-synthesis"
        )
        assert manifest["presentation_contract"]["source_mode"] == manifest["source_mode"]
        assert manifest["expression_profile"] == "source-led"
        assert set(manifest["prompts"][0]["blocks"]) == expected
        assert manifest["prompts"][0]["sources"][0]["sha256"]
        assert set(manifest["prompts"][0]["output_contract"]) == {"mime_type", "width", "height", "aspect_ratio"}
        assert "MUST REMOVE — plastic sign" in manifest["prompts"][0]["compiled_prompt"]
        assert manifest["privacy"]["upload_requires_explicit_consent"] is True
        assert manifest["generation_ready"] is True
        assert manifest["presentation_contract"]["image_generation_text_policy"] == "no-visible-text"
        assert manifest["system_display_name"]
    for system in ("cinematic-storyboard", "minimal-editorial", "editorial-sequence", "field-log", "museum-catalogue", "street-reportage", "fashion-editorial"):
        assert len(manifests[system]["prompts"]) == 2
    for system in ("memory-atlas", "family-archive", "travel-journal"):
        assert len(manifests[system]["prompts"]) == 1
    watercolor = compile_manifest(cards, "memory-atlas", source_root=tmp_path, expression_profile="watercolor-contour")
    assert "watercolor terrain" in watercolor["prompts"][0]["compiled_prompt"]
    assert "watercolor terrain" not in manifests["memory-atlas"]["prompts"][0]["compiled_prompt"]
    full_watercolor = compile_manifest(
        cards,
        "memory-atlas",
        source_root=tmp_path,
        expression_profile="full-watercolor-memory",
    )
    full_prompt = full_watercolor["prompts"][0]["compiled_prompt"]
    assert "full-watercolor-memory" in full_watercolor["available_expression_profiles"]
    assert "faces, skin, hair, clothing, objects, architecture, sky, water, and terrain" in full_prompt
    assert "medium-only transformation of the entire visible image" in full_prompt
    assert "Leave no photographic pixels" in full_prompt
    assert "one continuous hand-painted watercolor work" in full_prompt
    assert "recognizable painted anchor" in full_prompt
    assert "recognizable photographic anchor" not in full_prompt
    assert "MUST PRESERVE — person, rainy street" in full_prompt
    assert "MUST REMOVE — plastic sign" in full_prompt
    canonical = compile_manifest(cards, "memory-atlas", source_root=tmp_path, expression_profile="watercolor-chronicle")
    assert canonical["expression_profile"] == "watercolor-chronicle"
    assert full_watercolor["expression_profile_alias_for"] == "watercolor-chronicle"
    widescreen = compile_manifest(cards[:1], "cinematic-storyboard", source_root=tmp_path, aspect_ratio="16:9")
    contract = widescreen["prompts"][0]["output_contract"]
    assert contract["width"] * 9 == contract["height"] * 16


def test_single_photo_contract_stays_standalone_for_every_system_and_profile(tmp_path: Path):
    card = _cards(tmp_path)[0]
    card.direction.story_role = "moment"
    forbidden = (
        "sequence contract shared",
        "across the sequence",
        "across separate frames",
        "between frames",
        "continuity with adjacent beats",
        "follow source order",
        "connect places through",
        "every supplied source",
        "frame 01 /",
        "frame 01:",
    )
    for system in SUPPORTED_SYSTEMS:
        for profile in expression_profile_names(system):
            manifest = compile_manifest(
                [card],
                system,
                source_root=tmp_path,
                expression_profile=profile,
            )
            assert manifest["source_mode"] == "single-photo"
            assert manifest["presentation_contract"]["source_mode"] == "single-photo"
            assert manifest["sequence_review_required"] is False
            assert len(manifest["prompts"]) == 1
            assert manifest["prompts"][0]["output_contract"]["aspect_ratio"] == "3:2"
            prompt = manifest["prompts"][0]["compiled_prompt"].lower()
            assert not any(phrase in prompt for phrase in forbidden), (system, profile, prompt)
            assert "source / moment" in prompt or system in {
                "cinematic-storyboard",
                "minimal-editorial",
                "editorial-sequence",
                "field-log",
                "museum-catalogue",
                "street-reportage",
                "fashion-editorial",
            }


def test_new_systems_and_profiles_have_distinct_director_rules(tmp_path: Path):
    cards = _cards(tmp_path)
    expected_phrases = {
        "museum-catalogue": "inspectable catalogue plate",
        "travel-journal": "movement, pauses, thresholds",
        "street-reportage": "one reportage beat",
        "fashion-editorial": "editorial beat without inventing a brand campaign",
        "editorial-sequence": "sequencing, scale, pause, and contrast",
        "field-log": "field evidence",
    }
    compiled = {}
    for system, phrase in expected_phrases.items():
        manifest = compile_manifest(cards, system, source_root=tmp_path)
        prompt = manifest["prompts"][0]["compiled_prompt"]
        compiled[system] = prompt
        assert phrase in prompt
        assert "deterministic presentation layer" in prompt or system in {"travel-journal"}
    assert len({sha256(value.encode()).hexdigest() for value in compiled.values()}) == len(compiled)

    heritage = compile_manifest(cards, "family-archive", source_root=tmp_path, expression_profile="heritage-portrait")
    assert "silver-gelatin" in heritage["prompts"][0]["compiled_prompt"]
    assert "do not fabricate ancestry" in heritage["prompts"][0]["compiled_prompt"]
    dream = compile_manifest(cards, "fashion-editorial", source_root=tmp_path, expression_profile="dream-logic")
    dream_prompt = dream["prompts"][0]["compiled_prompt"]
    assert "one coherent impossible spatial rule" in dream_prompt
    assert "No random floating-object collage" in dream_prompt


def test_compiler_fails_closed_for_missing_source(tmp_path: Path):
    cards = _cards(tmp_path)
    (tmp_path / "bus-stop.jpg").unlink()
    with pytest.raises(FileNotFoundError):
        compile_manifest(cards, "minimal-editorial", source_root=tmp_path)


def test_upload_consent_waits_for_semantic_direction(tmp_path: Path):
    source = tmp_path / "generic.jpg"
    source.write_bytes(b"generic-source")
    card = SceneCard(
        source=source.name,
        width=1200,
        height=800,
        palette=["#888888"],
        brightness=.5,
        saturation=.1,
        orientation="landscape",
    )
    manifest = compile_manifest([card], "minimal-editorial", source_root=tmp_path)
    assert manifest["generation_ready"] is False
    with pytest.raises(ValueError, match="Semantic Scene Card direction is incomplete"):
        build_upload_consent(
            manifest,
            manifest_sha256="a" * 64,
            provider="example-provider",
            purpose="presentation synthesis",
            user_confirmed=True,
        )
    ready_manifest = compile_manifest(_cards(tmp_path)[:1], "minimal-editorial", source_root=tmp_path)
    ready_manifest["generation_ready"] = False
    with pytest.raises(ValueError, match="automatic route is unresolved"):
        build_upload_consent(
            ready_manifest,
            manifest_sha256="b" * 64,
            provider="example-provider",
            purpose="presentation synthesis",
            user_confirmed=True,
        )


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


def test_review_template_and_final_record_close_the_accept_path(tmp_path: Path):
    candidate = tmp_path / "candidate.png"
    Image.new("RGB", (1536, 1024), "navy").save(candidate)
    prompt_manifest = compile_manifest(_cards(tmp_path)[:1], "minimal-editorial", source_root=tmp_path)
    render_manifest = bind_outputs(
        prompt_manifest,
        {"minimal-editorial-01": str(candidate)},
        manifest_sha256="a" * 64,
    )
    manifest_hash = sha256(json.dumps(render_manifest, sort_keys=True).encode()).hexdigest()
    template = build_review_template(
        render_manifest,
        manifest_sha256=manifest_hash,
        reviewer_type="human",
        reviewer_name="test reviewer",
        reviewer_model="visual inspection",
        review_method="full-resolution comparison",
    )
    assert template["results"][0]["output_sha256"] == render_manifest["prompts"][0]["candidate_output"]["sha256"]
    template["results"][0]["scores"] = {
        name: 4 for name in render_manifest["review_policy"]["dimensions"]
    }
    record = build_review_record(render_manifest, template, manifest_sha256=manifest_hash)
    assert record["artifact_type"] == "aesthetic-review"
    assert record["decision"] == "accept"
    assert record["results"][0]["decision"] == "accept"
    assert record["failed_prompt_ids"] == []


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
    assessment_path = tmp_path / "assessment.json"
    assert main([
        "review-template", str(bound_path),
        "--reviewer-type", "human",
        "--reviewer-name", "test reviewer",
        "--reviewer-model", "visual inspection",
        "--method", "full-resolution comparison",
        "-o", str(assessment_path),
    ]) == 0
    assessment = json.loads(assessment_path.read_text())
    assessment["results"][0]["scores"] = {
        name: 5 for name in bound["review_policy"]["dimensions"]
    }
    assessment_path.write_text(json.dumps(assessment))
    review_path = tmp_path / "review.json"
    assert main(["review", str(bound_path), str(assessment_path), "-o", str(review_path)]) == 0
    assert json.loads(review_path.read_text())["decision"] == "accept"
    retry_path = tmp_path / "retry.json"
    assert main(["retry", str(bound_path), str(review_path), "-o", str(retry_path)]) == 0
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
    def digest(path: Path) -> str:
        return sha256(path.read_bytes()).hexdigest()
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
