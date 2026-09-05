import base64
import hashlib
import json
import re
from pathlib import Path

import pytest
from PIL import Image, ImageChops, ImageStat

import moments_to_pages.render as renderer
import moments_to_pages.workflow as workflow
import moments_to_pages.image_safety as image_safety
from moments_to_pages.cli import main
from moments_to_pages.model import (
    Direction,
    Interpretation,
    Observation,
    SceneCard,
    load_cards,
)
from moments_to_pages.workflow import select_direct_route


def _story(tmp_path: Path, count: int = 3) -> Path:
    photos = tmp_path / "photos"
    photos.mkdir()
    items = []
    for index in range(count):
        photo = photos / f"frame {index}#.png"
        Image.new("RGB", (320, 200), (30 + index * 20, 60, 90)).save(photo)
        items.append({
            "source": f"photos/{photo.name}", "width": 320, "height": 200,
            "palette": ["#1E3C5A"], "brightness": 0.4, "saturation": 0.3,
            "orientation": "landscape", "caption": f"FRAME {index}",
        })
    story = tmp_path / "story.json"
    story.write_text(json.dumps(items))
    return story


def test_story_relative_paths_and_default_extension(tmp_path: Path, monkeypatch):
    story = _story(tmp_path)
    assert Path(load_cards(story)[0].source).exists()
    monkeypatch.chdir(tmp_path)
    assert main(["render", str(story), "--format", "png"]) == 0
    assert (tmp_path / "story.png").exists()


def test_analyze_paths_are_relative_to_nested_story(tmp_path: Path, monkeypatch):
    photo = tmp_path / "photos" / "a.png"
    photo.parent.mkdir()
    Image.new("RGB", (40, 30), "red").save(photo)
    monkeypatch.chdir(tmp_path)
    story = tmp_path / "out" / "story.json"
    assert main(["analyze", "photos/a.png", "-o", str(story)]) == 0
    analyzed = json.loads(story.read_text())[0]
    assert analyzed["source"] == "../photos/a.png"
    assert analyzed["direction"]["story_role"] == "moment"
    assert Path(load_cards(story)[0].source) == photo
    manifest = tmp_path / "out" / "manifest.json"
    assert main(["compile", str(story), "--system", "minimal-editorial", "-o", str(manifest)]) == 0
    assert json.loads(manifest.read_text())["prompts"][0]["sources"][0]["sha256"]


def test_nested_manifests_keep_story_candidates_and_svg_portable(tmp_path: Path, monkeypatch):
    story = _story(tmp_path, 1)
    monkeypatch.chdir(tmp_path)
    prompt_path = tmp_path / "bundle" / "manifests" / "prompt-manifest.json"
    assert main([
        "compile", str(story.resolve()), "--system", "minimal-editorial", "-o", str(prompt_path)
    ]) == 0
    prompt = json.loads(prompt_path.read_text())
    assert str(tmp_path) not in prompt["story"]
    assert (prompt_path.parent / prompt["story"]).resolve() == story.resolve()

    candidate = tmp_path / "outputs" / "candidate.png"
    candidate.parent.mkdir()
    Image.new("RGB", (1536, 1024), "navy").save(candidate)
    render_path = tmp_path / "bundle" / "review" / "render-manifest.json"
    assert main([
        "bind-outputs", str(prompt_path),
        "--result", "minimal-editorial-01=outputs/candidate.png",
        "-o", str(render_path),
    ]) == 0
    render_manifest = json.loads(render_path.read_text())
    stored = render_manifest["prompts"][0]["candidate_output"]["path"]
    assert not Path(stored).is_absolute()
    assert (render_path.parent / stored).resolve() == candidate.resolve()

    presentation = tmp_path / "bundle" / "presentation" / "result.svg"
    assert main(["present", str(render_path), "-o", str(presentation)]) == 0
    svg = presentation.read_text()
    assert "file:///" not in svg and "file%3A///" not in svg
    assert str(tmp_path) not in svg


def test_bundled_skill_can_be_located_and_copied(tmp_path: Path, capsys):
    assert main(["skill-path"]) == 0
    source = Path(capsys.readouterr().out.strip())
    assert (source / "SKILL.md").is_file()
    destination = tmp_path / "installed" / "scene-card-studio"
    assert main(["install-skill", "--target", str(destination)]) == 0
    assert (destination / "SKILL.md").is_file()
    assert not list(destination.rglob("*.pyc"))
    with pytest.raises(SystemExit, match="Refusing to overwrite"):
        main(["install-skill", "--target", str(destination)])


def test_analysis_rejects_images_over_the_pixel_limit(tmp_path: Path, monkeypatch):
    image = tmp_path / "large.png"
    Image.new("RGB", (20, 20), "navy").save(image)
    monkeypatch.setattr(image_safety, "MAX_RASTER_PIXELS", 100)
    with pytest.raises(ValueError, match="pixel safety limit"):
        main(["analyze", str(image), "-o", str(tmp_path / "story.json")])


def test_profiles_command_and_nested_output_directories(tmp_path: Path, capsys):
    story = _story(tmp_path, 1)
    assert main(["profiles", "--system", "family-archive"]) == 0
    output = capsys.readouterr().out
    assert "family-archive" in output
    assert "source-led" in output
    assert "watercolor-chronicle" in output
    assert "heritage-portrait" in output

    nested = tmp_path / "new" / "deep" / "prompt-manifest.json"
    assert main([
        "compile",
        str(story),
        "--system",
        "family-archive",
        "--expression-profile",
        "heritage-portrait",
        "-o",
        str(nested),
    ]) == 0
    assert nested.exists()
    assert json.loads(nested.read_text())["source_mode"] == "single-photo"
    rendered = tmp_path / "another" / "deep" / "workprint.png"
    assert main(["render", str(story), "--format", "png", "-o", str(rendered)]) == 0
    assert rendered.exists()


def test_direct_command_creates_portable_local_bundle_without_claiming_generation(tmp_path: Path, capsys):
    photo = tmp_path / "portrait.png"
    Image.new("RGB", (360, 540), (120, 145, 170)).save(photo)
    output = tmp_path / "direct-run"
    assert main([
        "direct",
        str(photo),
        "--brief",
        "把这张家庭肖像处理成克制银盐与手工着色的传统影像肖像。",
        "-o",
        str(output),
    ]) == 0
    assert {path.name for path in output.iterdir()} == {
        "story.json", "prompt-manifest.json", "workprint.svg", "run-summary.json"
    }
    story = json.loads((output / "story.json").read_text())
    manifest = json.loads((output / "prompt-manifest.json").read_text())
    summary = json.loads((output / "run-summary.json").read_text())
    assert story[0]["source"] == "../portrait.png"
    assert story[0]["direction"]["story_role"] == "moment"
    assert manifest["source_mode"] == "single-photo"
    assert manifest["system"] == "family-archive"
    assert manifest["expression_profile"] == "heritage-portrait"
    assert summary["generation"]["remote_generation_performed"] is False
    assert summary["generation"]["workprint_is_directed_after"] is False
    assert summary["direction_readiness"]["generation_ready"] is False
    assert summary["generation"]["status"] == "needs-semantic-direction"
    assert main(["check", str(output / "story.json")]) == 2
    output_text = capsys.readouterr().out
    assert "No source photo was uploaded" in output_text


def test_direct_accepts_matching_prepared_semantic_scene_cards(tmp_path: Path):
    photo = tmp_path / "portrait.png"
    Image.new("RGB", (360, 540), (120, 145, 170)).save(photo)
    output = tmp_path / "direct-run"
    assert main(["direct", str(photo), "--brief", "quiet portrait", "-o", str(output)]) == 0
    story_path = output / "story.json"
    story = json.loads(story_path.read_text())
    story[0]["observation"] = {
        "subjects": ["seated person", "woven chair"],
        "dominant_gesture": "hands resting above crossed ankles",
        "quiet_regions": ["plain wall above the sitter"],
    }
    story[0]["interpretation"] = {
        "narrative_intent": "a restrained study of presence",
        "emotional_tone": ["calm", "attentive"],
        "confidence": 0.9,
        "method": "model-assisted-and-user-reviewed",
    }
    story[0]["direction"] = {
        "story_role": "moment",
        "director_note": "Keep identity and pose exact; direct attention through material restraint.",
        "layout_emphasis": "face, hands, and chair geometry",
    }
    story[0]["transformation"] = {
        "must_preserve": ["identity", "pose", "hands", "woven chair"],
        "may_transform": ["crop", "light", "background clutter"],
        "must_remove": [],
    }
    story_path.write_text(json.dumps(story))
    assert main([
        "direct", str(photo), "--brief", "quiet portrait", "--scene-cards", str(story_path),
        "-o", str(output), "--force",
    ]) == 0
    summary = json.loads((output / "run-summary.json").read_text())
    manifest = json.loads((output / "prompt-manifest.json").read_text())
    assert summary["direction_readiness"]["generation_ready"] is True
    assert summary["generation"]["status"] == "prompt-ready"
    assert summary["prepared_story"]["provided"] is True
    assert len(summary["prepared_story"]["sha256"]) == 64
    assert str(tmp_path) not in (output / "run-summary.json").read_text()
    assert manifest["generation_ready"] is True
    assert main(["check", str(output / "story.json")]) == 0


def test_direct_rejects_prepared_story_for_different_sources(tmp_path: Path):
    first = tmp_path / "first.png"
    second = tmp_path / "second.png"
    Image.new("RGB", (100, 100), "red").save(first)
    Image.new("RGB", (100, 100), "blue").save(second)
    prepared = tmp_path / "prepared"
    assert main(["direct", str(first), "-o", str(prepared)]) == 0
    with pytest.raises(SystemExit, match="sources must match"):
        main([
            "direct", str(second), "--scene-cards", str(prepared / "story.json"),
            "-o", str(tmp_path / "mismatch"),
        ])


def test_direct_command_refuses_accidental_overwrite(tmp_path: Path):
    photo = tmp_path / "photo.png"
    Image.new("RGB", (100, 100), "gray").save(photo)
    output = tmp_path / "run"
    assert main(["direct", str(photo), "-o", str(output)]) == 0
    with pytest.raises(SystemExit, match="Direct output already exists"):
        main(["direct", str(photo), "-o", str(output)])
    assert main(["direct", str(photo), "-o", str(output), "--force"]) == 0


def test_direct_auto_system_respects_an_explicit_compatible_profile(tmp_path: Path):
    photo = tmp_path / "photo.png"
    Image.new("RGB", (120, 180), "gray").save(photo)
    output = tmp_path / "watercolor"
    assert main([
        "direct", str(photo), "--expression-profile", "watercolor-chronicle", "-o", str(output)
    ]) == 0
    summary = json.loads((output / "run-summary.json").read_text())
    assert summary["route"]["system"] in {
        "memory-atlas", "family-archive", "museum-catalogue", "travel-journal"
    }
    assert summary["route"]["expression_profile"] == "watercolor-chronicle"
    assert summary["route"]["system_selection"] == "automatic-compatible-with-profile"


def test_direct_force_refuses_symlink_output_targets(tmp_path: Path):
    photo = tmp_path / "photo.png"
    Image.new("RGB", (100, 100), "gray").save(photo)
    output = tmp_path / "run"
    output.mkdir()
    outside = tmp_path / "outside.json"
    (output / "story.json").symlink_to(outside)
    with pytest.raises(SystemExit, match="Refusing to replace non-regular"):
        main(["direct", str(photo), "-o", str(output), "--force"])
    assert not outside.exists()


def test_direct_invalid_contract_does_not_leave_a_partial_bundle(tmp_path: Path):
    photo = tmp_path / "photo.png"
    Image.new("RGB", (100, 100), "gray").save(photo)
    output = tmp_path / "invalid"
    with pytest.raises(SystemExit, match="aspect ratio"):
        main([
            "direct", str(photo), "--aspect-ratio", "not-a-ratio", "-o", str(output)
        ])
    assert output.is_dir()
    assert not any(output.iterdir())


def test_direct_force_preserves_previous_bundle_when_workprint_fails(tmp_path: Path, monkeypatch):
    photo = tmp_path / "photo.png"
    Image.new("RGB", (100, 100), "gray").save(photo)
    output = tmp_path / "run"
    assert main(["direct", str(photo), "-o", str(output)]) == 0
    original = {path.name: path.read_bytes() for path in output.iterdir()}

    def fail_render(*args, **kwargs):
        raise RuntimeError("simulated workprint failure")

    monkeypatch.setattr(workflow, "render_svg", fail_render)
    with pytest.raises(RuntimeError, match="simulated workprint failure"):
        main(["direct", str(photo), "-o", str(output), "--force"])
    assert {path.name: path.read_bytes() for path in output.iterdir()} == original


def test_direct_workprint_names_the_selected_system_not_only_its_layout_family(tmp_path: Path):
    photo = tmp_path / "object.png"
    Image.new("RGB", (180, 240), "gray").save(photo)
    output = tmp_path / "museum"
    assert main([
        "direct", str(photo), "--system", "museum-catalogue", "-o", str(output)
    ]) == 0
    svg = (output / "workprint.svg").read_text()
    assert "MUSEUM CATALOGUE" in svg
    assert "SYSTEM museum-catalogue · PROFILE source-led · ANALYSIS WORKPRINT" in svg


def test_bilingual_direct_brief_eval_matrix_routes_every_system_and_profile():
    root = Path(__file__).resolve().parents[1]
    matrix = json.loads((root / "evals/direct-briefs.json").read_text())
    card = SceneCard(
        source="fixture.png",
        width=1200,
        height=800,
        palette=["#858B92", "#D8D5CC"],
        brightness=.55,
        saturation=.18,
        orientation="landscape",
        observation=Observation(),
        interpretation=Interpretation(),
        direction=Direction(),
    )
    routed_systems = set()
    routed_profiles = set()
    for case in matrix["cases"]:
        route = select_direct_route([card], brief=case["brief"])
        assert route["system"] == case["system"], case["id"]
        assert route["expression_profile"] == case["expression_profile"], case["id"]
        routed_systems.add(route["system"])
        routed_profiles.add(route["expression_profile"])
    assert routed_systems == {
        "cinematic-storyboard", "memory-atlas", "family-archive", "minimal-editorial",
        "editorial-sequence", "field-log", "museum-catalogue", "travel-journal",
        "journey-taxonomy", "street-reportage", "fashion-editorial",
    }
    assert routed_profiles >= {
        "source-led", "rain-nocturne", "quiet-window-light", "watercolor-contour",
        "watercolor-chronicle", "graphite-paper", "heritage-portrait",
        "monochrome-reportage", "dream-logic", "mineral-ink-memory",
        "impasto-light-study", "pixel-diary", "risograph-route",
        "gouache-place-study", "cyanotype-archive", "paper-relief-landscape",
        "sculpted-place-diorama", "threaded-landscape", "autochrome-memory", "pixel-ink-memory",
    }
    for case in matrix["adversarial_cases"]:
        route = select_direct_route([card], brief=case["brief"])
        assert route["system"] == case["system"], case["id"]
        assert route["expression_profile"] == case["expression_profile"], case["id"]
        assert route["needs_route_confirmation"] is case["needs_route_confirmation"], case["id"]
    for case in matrix["ambiguous_cases"]:
        route = select_direct_route([card], brief=case["brief"])
        assert route["needs_route_confirmation"] is case["needs_route_confirmation"], case["id"]


def test_direct_routing_respects_negation_and_flags_real_ties():
    card = SceneCard(
        source="fixture.png",
        width=1200,
        height=800,
        palette=["#858B92"],
        brightness=.55,
        saturation=.18,
        orientation="landscape",
        observation=Observation(),
        interpretation=Interpretation(),
        direction=Direction(),
    )
    negative = select_direct_route(
        [card],
        brief="不要电影感，也不要水彩；做安静极简静物，强调材质与留白。",
    )
    assert negative["system"] == "minimal-editorial"
    assert negative["expression_profile"] == "source-led"
    assert negative["needs_route_confirmation"] is False

    ambiguous = select_direct_route([card], brief="Make it cinematic and minimal.")
    assert ambiguous["needs_route_confirmation"] is True
    explicit = select_direct_route(
        [card], brief="Make it cinematic and minimal.", system="minimal-editorial"
    )
    assert explicit["system"] == "minimal-editorial"
    assert explicit["needs_route_confirmation"] is False

    low_confidence = select_direct_route([card], brief="Keep this portrait faithful and restrained.")
    assert low_confidence["system_score"] < .8
    assert low_confidence["needs_route_confirmation"] is True
    assert low_confidence["route_confirmation_reason"] == "low-system-confidence"


def test_deterministic_presentation_uses_only_bound_metadata(tmp_path: Path, monkeypatch):
    story = _story(tmp_path, 1)
    data = json.loads(story.read_text())
    data[0]["metadata"] = {"location": "Harbor Road", "date": "2026-08-10", "catalogue_id": "SCS-001"}
    story.write_text(json.dumps(data))
    manifest = tmp_path / "prompt-manifest.json"
    assert main(["compile", str(story), "--system", "museum-catalogue", "-o", str(manifest)]) == 0
    prompt = json.loads(manifest.read_text())["prompts"][0]
    candidate = tmp_path / "candidate.png"
    contract = prompt["output_contract"]
    Image.new("RGB", (contract["width"], contract["height"]), "navy").save(candidate)
    monkeypatch.chdir(tmp_path)
    render_manifest = tmp_path / "render-manifest.json"
    assert main([
        "bind-outputs", str(manifest), "--result", f"{prompt['id']}={candidate.name}", "-o", str(render_manifest)
    ]) == 0
    presentation = tmp_path / "presentation.svg"
    assert main(["present", str(render_manifest), "-o", str(presentation)]) == 0
    svg = presentation.read_text()
    assert "MUSEUM CATALOGUE" in svg.upper()
    assert "Harbor Road" in svg
    assert "2026-08-10" in svg
    assert "SCS-001" in svg
    assert "invented place" not in svg


def test_journey_keepsake_is_asymmetric_and_uses_only_supplied_metadata(tmp_path: Path, monkeypatch):
    story = _story(tmp_path, 1)
    data = json.loads(story.read_text())
    data[0]["caption"] = "TIDAL PATH"
    data[0]["metadata"] = {
        "location": "North Marsh",
        "date": "2026-08-10",
        "source_note": "Boardwalk after rain",
    }
    story.write_text(json.dumps(data))
    manifest = tmp_path / "prompt-manifest.json"
    assert main(["compile", str(story), "--system", "travel-journal", "-o", str(manifest)]) == 0
    prompt = json.loads(manifest.read_text())["prompts"][0]
    candidate = tmp_path / "candidate.png"
    contract = prompt["output_contract"]
    Image.new("RGB", (contract["width"], contract["height"]), "navy").save(candidate)
    monkeypatch.chdir(tmp_path)
    render_manifest = tmp_path / "render-manifest.json"
    assert main([
        "bind-outputs", str(manifest), "--result", f"{prompt['id']}={candidate.name}", "-o", str(render_manifest)
    ]) == 0
    presentation = tmp_path / "journey-keepsake.svg"
    assert main([
        "present", str(render_manifest), "--style", "journey-keepsake", "-o", str(presentation)
    ]) == 0
    svg = presentation.read_text()
    assert 'data-presentation-style="journey-keepsake"' in svg
    assert "TIDAL PATH" in svg
    assert "North Marsh" in svg and "2026-08-10" in svg and "Boardwalk after rain" in svg
    assert "WANDERLUST" not in svg and "Evening Wind" not in svg
    assert 'x1="302"' in svg


def test_ink_poetry_presentation_splits_only_supplied_title_and_verse(tmp_path: Path, monkeypatch):
    story = _story(tmp_path, 1)
    data = json.loads(story.read_text())
    data[0]["caption"] = "静观｜窗影入墨，闲看岁长"
    story.write_text(json.dumps(data))
    manifest = tmp_path / "prompt-manifest.json"
    assert main([
        "compile", str(story), "--system", "memory-atlas",
        "--expression-profile", "chinese-ink-poetry", "-o", str(manifest),
    ]) == 0
    prompt = json.loads(manifest.read_text())["prompts"][0]
    candidate = tmp_path / "candidate.png"
    contract = prompt["output_contract"]
    Image.new("RGB", (contract["width"], contract["height"]), "ivory").save(candidate)
    monkeypatch.chdir(tmp_path)
    render_manifest = tmp_path / "render-manifest.json"
    assert main([
        "bind-outputs", str(manifest), "--result", f"{prompt['id']}={candidate.name}", "-o", str(render_manifest)
    ]) == 0
    presentation = tmp_path / "ink-poetry.svg"
    assert main([
        "present", str(render_manifest), "--style", "ink-poetry", "-o", str(presentation)
    ]) == 0
    svg = presentation.read_text()
    assert 'data-presentation-style="ink-poetry"' in svg
    assert "静观" in svg and "窗影入墨，闲看岁长" in svg
    assert "｜" not in svg
    assert "writing-mode:vertical-rl" in svg
    assert "山静云闲" not in svg


def test_svg_systems_are_distinct_and_paths_are_output_relative(tmp_path: Path):
    story = _story(tmp_path)
    hashes = set()
    for system in ("source-contact-sheet", "editorial-sequence", "family-archive", "memory-atlas", "field-log"):
        output = tmp_path / f"{system}.svg"
        main(["render", str(story), "--style", system, "--format", "svg", "-o", str(output)])
        data = output.read_bytes()
        hashes.add(hashlib.sha256(data).hexdigest())
        assert "photos/frame%200%23.png" in output.read_text() or system == "memory-atlas"
    assert len(hashes) == 5


@pytest.mark.parametrize("system, point", [
    ("field-log", (100, 240 + 11 * 440 + 20)),
    ("memory-atlas", (900, 330 + 11 * 260 + 20)),
])
def test_dynamic_png_contains_last_of_twelve_frames(tmp_path: Path, system: str, point: tuple[int, int]):
    story = _story(tmp_path, 12)
    output = tmp_path / f"twelve-{system}.png"
    main(["render", str(story), "--style", system, "--format", "png", "-o", str(output)])
    with Image.open(output) as image:
        expected = (30 + 11 * 20, 60, 90)
        actual = image.getpixel(point)
        assert all(abs(a - b) < 5 for a, b in zip(actual, expected))


def test_embed_images_are_safely_reencoded_and_external_sources_are_rejected(tmp_path: Path, monkeypatch):
    story = _story(tmp_path, 2)
    monkeypatch.chdir(tmp_path)
    output = tmp_path / "embedded.svg"
    assert main(["render", str(story), "--style", "memory-atlas", "--format", "svg", "--embed-images", "-o", str(output)]) == 0
    assert output.read_text().count("data:image/png;base64,") == 2

    tailed = tmp_path / "photos" / "tailed.png"
    Image.new("RGB", (30, 20), "orange").save(tailed)
    secret = b"PRIVATE_TEXT_AFTER_PNG_END"
    tailed.write_bytes(tailed.read_bytes() + secret)
    data = json.loads(story.read_text())
    data[0]["source"] = "photos/tailed.png"
    story.write_text(json.dumps(data))
    sanitized = tmp_path / "sanitized.svg"
    main(["render", str(story), "--format", "svg", "--embed-images", "-o", str(sanitized)])
    payload = re.search(r"data:image/png;base64,([A-Za-z0-9+/=]+)", sanitized.read_text()).group(1)
    decoded = base64.b64decode(payload)
    assert secret not in decoded

    external = tmp_path.parent / "outside-scene-card.png"
    Image.new("RGB", (20, 20), "blue").save(external)
    data = json.loads(story.read_text())
    data[0]["source"] = str(external)
    story.write_text(json.dumps(data))
    with pytest.raises(PermissionError):
        main(["render", str(story), "--format", "svg", "--embed-images", "-o", str(tmp_path / "blocked.svg")])

    disguised = tmp_path / "not-an-image.png"
    disguised.write_text("private text must never be embedded as an image")
    data[0]["source"] = "not-an-image.png"
    story.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="decodable raster image"):
        main(["render", str(story), "--format", "svg", "--embed-images", "-o", str(tmp_path / "disguised.svg")])

    data[0]["source"] = "photos/tailed.png"
    story.write_text(json.dumps(data))
    monkeypatch.setattr(renderer, "MAX_EMBED_SOURCE_BYTES", 1)
    with pytest.raises(ValueError, match="bytes"):
        main(["render", str(story), "--format", "svg", "--embed-images", "-o", str(tmp_path / "too-large.svg")])
    monkeypatch.setattr(renderer, "MAX_EMBED_SOURCE_BYTES", 25 * 1024 * 1024)
    monkeypatch.setattr(renderer, "MAX_EMBED_PIXELS", 10)
    with pytest.raises(ValueError, match="pixels"):
        main(["render", str(story), "--format", "svg", "--embed-images", "-o", str(tmp_path / "too-many-pixels.svg")])


def test_renderer_has_no_case_copy_and_layout_emphasis_changes_layout(tmp_path: Path):
    story = _story(tmp_path, 2)
    first = tmp_path / "first.svg"
    main(["render", str(story), "--style", "editorial-sequence", "--format", "svg", "-o", str(first)])
    data = json.loads(story.read_text())
    data[1]["direction"] = {"layout_emphasis": "primary person", "story_role": "closing", "director_note": "Keep it primary."}
    story.write_text(json.dumps(data))
    second = tmp_path / "second.svg"
    main(["render", str(story), "--style", "editorial-sequence", "--format", "svg", "-o", str(second)])
    assert hashlib.sha256(first.read_bytes()).digest() != hashlib.sha256(second.read_bytes()).digest()

    renderer_source = (Path(__file__).resolve().parents[1] / "src/moments_to_pages/render.py").read_text()
    for leaked in ("CARE → PAUSE → DEPARTURE", "Laundry / shared work", "coastal-memory-atlas.png"):
        assert leaked not in renderer_source


def test_published_single_photo_galleries_have_valid_roles_and_distinct_pairs():
    root = Path(__file__).resolve().parents[1]
    for gallery_name, expected_count in (("v0.4-gallery", 13), ("v0.6-gallery", 12)):
        gallery = root / "examples/cases" / gallery_name
        records = json.loads((gallery / "case-records.json").read_text())
        assert len(records["cases"]) == expected_count
        for case in records["cases"]:
            assert case["scene_card"]["direction"]["story_role"] == "moment"
            before = gallery / case["before"]
            after = gallery / case["after"]
            assert before.is_file()
            assert after.is_file()
            assert hashlib.sha256(before.read_bytes()).digest() != hashlib.sha256(after.read_bytes()).digest()
            with Image.open(before) as before_image, Image.open(after) as after_image:
                before_rgb = before_image.convert("RGB").resize((128, 128))
                after_rgb = after_image.convert("RGB").resize((128, 128))
                difference = ImageStat.Stat(ImageChops.difference(before_rgb, after_rgb))
                normalized_mean_difference = sum(difference.mean) / (3 * 255)
            assert normalized_mean_difference >= .06, case["case_id"]
