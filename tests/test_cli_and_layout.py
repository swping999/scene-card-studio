import hashlib
import json
from pathlib import Path

from PIL import Image

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


def test_dynamic_png_contains_last_of_twelve_frames(tmp_path: Path):
    story = _story(tmp_path, 12)
    output = tmp_path / "twelve.png"
    main(["render", str(story), "--style", "field-log", "--format", "png", "-o", str(output)])
    with Image.open(output) as image:
        assert image.height >= 300 + 12 * 440
