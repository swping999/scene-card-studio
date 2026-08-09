from pathlib import Path

from moments_to_pages.director import recommend_systems
from moments_to_pages.model import Direction, SceneCard, load_cards, save_cards
from moments_to_pages.render import render_png, render_svg


def test_roundtrip_and_render(tmp_path: Path):
    photo = tmp_path / "photo.jpg"
    photo.write_bytes(b"placeholder")
    cards = [SceneCard(str(photo), 1200, 800, ["#E6533C", "#263B47"], .6, .3, "landscape", "SEA WIND", direction=Direction(story_role="opening"))]
    story = tmp_path / "story.json"
    output = tmp_path / "story.svg"
    save_cards(cards, story)
    render_svg(load_cards(story), output, "field-notes")
    result = output.read_text()
    assert "SEA WIND" in result
    assert "SCENE CARD STUDIO" in result
    assert result.endswith("</svg>\n")
    assert recommend_systems(cards)[0].system in {"editorial-sequence", "memory-atlas", "field-log"}
