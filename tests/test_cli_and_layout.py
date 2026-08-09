import hashlib
import json
import base64
import re
from pathlib import Path

import pytest
from PIL import Image

import moments_to_pages.render as renderer
from moments_to_pages.cli import main
from moments_to_pages.model import load_cards


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
    assert json.loads(story.read_text())[0]["source"] == "../photos/a.png"
    assert Path(load_cards(story)[0].source) == photo
    manifest = tmp_path / "out" / "manifest.json"
    assert main(["compile", str(story), "--system", "minimal-editorial", "-o", str(manifest)]) == 0
    assert json.loads(manifest.read_text())["prompts"][0]["sources"][0]["sha256"]


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
