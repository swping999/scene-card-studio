import base64
import hashlib
import json
import re
from pathlib import Path

import pytest
from PIL import Image, ImageChops, ImageStat

import moments_to_pages.render as renderer
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
    output_text = capsys.readouterr().out
    assert "No source photo was uploaded" in output_text


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
        "street-reportage", "fashion-editorial",
    }
    assert routed_profiles >= {
        "source-led", "rain-nocturne", "quiet-window-light", "watercolor-contour",
        "watercolor-chronicle", "graphite-paper", "heritage-portrait",
        "monochrome-reportage", "dream-logic",
    }


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


def test_published_single_photo_gallery_has_valid_roles_and_distinct_pairs():
    root = Path(__file__).resolve().parents[1]
    gallery = root / "examples/cases/v0.4-gallery"
    records = json.loads((gallery / "case-records.json").read_text())
    assert len(records["cases"]) == 13
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
        assert normalized_mean_difference >= .06, case["id"]
