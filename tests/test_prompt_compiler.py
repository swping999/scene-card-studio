import json
from pathlib import Path

from moments_to_pages.cli import main
from moments_to_pages.director import recommend_systems
from moments_to_pages.model import Direction, Interpretation, Observation, SceneCard
from moments_to_pages.prompt_compiler import SUPPORTED_SYSTEMS, compile_manifest
from moments_to_pages.review import build_retry_manifest, review_decision


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
                subjects=["person", "rainy street"],
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
        ))
    return cards


def test_four_systems_compile_with_required_blocks(tmp_path: Path):
    cards = _cards(tmp_path)
    expected = {
        "subject_fidelity", "narrative_intent", "composition", "lighting", "material",
        "spatial_relationships", "text_strategy", "exclusions", "output",
    }
    manifests = {}
    for system in SUPPORTED_SYSTEMS:
        manifest = compile_manifest(cards, system, source_root=tmp_path)
        manifests[system] = manifest
        assert manifest["compiler_version"] == "0.3.0"
        assert set(manifest["prompts"][0]["blocks"]) == expected
        assert manifest["prompts"][0]["sources"][0]["sha256"]
        assert "SUBJECT FIDELITY" in manifest["prompts"][0]["compiled_prompt"]
    assert len(manifests["cinematic-storyboard"]["prompts"]) == 2
    assert len(manifests["minimal-editorial"]["prompts"]) == 2
    assert len(manifests["memory-atlas"]["prompts"]) == 1
    assert len(manifests["family-archive"]["prompts"]) == 1
    assert "movie poster" in manifests["cinematic-storyboard"]["prompts"][0]["compiled_prompt"]
    assert "watercolor terrain" in manifests["memory-atlas"]["prompts"][0]["compiled_prompt"]


def test_review_builds_targeted_retry_only_for_failed_dimensions(tmp_path: Path):
    manifest = compile_manifest(_cards(tmp_path)[:1], "minimal-editorial", source_root=tmp_path)
    prompt_id = manifest["prompts"][0]["id"]
    assessment = {"results": [{
        "prompt_id": prompt_id,
        "scores": {
            "subject_fidelity": 5,
            "narrative_alignment": 4,
            "composition": 3,
            "system_distinctiveness": 4,
            "artifact_control": 2,
        },
        "notes": "Remove the synthetic cable and restore the chair legs.",
    }]}
    retry = build_retry_manifest(manifest, assessment)
    assert retry["retry_prompt_ids"] == [prompt_id]
    prompt = retry["prompts"][0]["compiled_prompt"]
    assert "composition:" in prompt
    assert "artifact_control:" in prompt
    assert "subject_fidelity:" not in prompt.split("TARGETED CORRECTION PASS", 1)[1]
    assert review_decision({name: 4 for name in manifest["review_policy"]["dimensions"]}) == ("accept", [])


def test_cli_compiles_and_retries(tmp_path: Path):
    cards = _cards(tmp_path)[:1]
    story = tmp_path / "story.json"
    story.write_text(json.dumps([card.to_dict() for card in cards]))
    manifest_path = tmp_path / "prompts.json"
    assert main(["compile", str(story), "--system", "cinematic-storyboard", "-o", str(manifest_path)]) == 0
    manifest = json.loads(manifest_path.read_text())
    prompt_id = manifest["prompts"][0]["id"]
    assessment_path = tmp_path / "assessment.json"
    assessment_path.write_text(json.dumps({"results": [{
        "prompt_id": prompt_id,
        "scores": {name: 5 for name in manifest["review_policy"]["dimensions"]},
    }]}))
    retry_path = tmp_path / "retry.json"
    assert main(["retry", str(manifest_path), str(assessment_path), "-o", str(retry_path)]) == 0
    assert json.loads(retry_path.read_text())["retry_prompt_ids"] == []


def test_recommender_distinguishes_cinematic_and_minimal(tmp_path: Path):
    cinematic = _cards(tmp_path)
    assert recommend_systems(cinematic)[0].system == "cinematic-storyboard"

    minimal = _cards(tmp_path)
    for card, subject in zip(minimal, ("ceramic mug", "folded linen")):
        card.observation.subjects = [subject, "material surface"]
        card.observation.dominant_gesture = "object held in negative space"
        card.interpretation.narrative_intent = "quiet material study"
        card.interpretation.emotional_tone = ["quiet", "tactile"]
        card.direction.director_note = "Preserve wear and remove accidental clutter."
    assert recommend_systems(minimal)[0].system == "minimal-editorial"
