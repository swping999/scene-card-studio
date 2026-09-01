from pathlib import Path

import pytest

from moments_to_pages.director import recommend_systems
from moments_to_pages.model import (
    Direction,
    SceneCard,
    SourceMetadata,
    load_cards,
    save_cards,
)
from moments_to_pages.narrative_systems import SUPPORTED_SYSTEMS
from moments_to_pages.render import render_svg


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
    assert recommend_systems(cards)[0].system in SUPPORTED_SYSTEMS


def test_scene_card_rejects_illegal_svg_controls(tmp_path: Path):
    card = SceneCard("photo.jpg", 10, 10, ["#112233"], .5, .5, "landscape", "BAD\x01CAPTION")
    with pytest.raises(ValueError, match="control character"):
        save_cards([card], tmp_path / "story.json")


def test_mixed_legacy_and_current_schema_migrates_without_direction_crash():
    value = SceneCard(
        "photo.jpg", 10, 10, ["#112233"], .5, .5, "landscape", "MOMENT"
    ).to_dict()
    value["interpretation"]["narrative_intent"] = "current reading"
    value["direction"]["narrative_intent"] = "legacy reading"
    value["direction"]["emotional_tone"] = ["legacy tone"]
    value["direction"]["confidence"] = 0.2
    card = SceneCard.from_dict(value)
    assert card.interpretation.narrative_intent == "current reading"
    assert card.interpretation.emotional_tone == value["interpretation"]["emotional_tone"]


def test_supplied_metadata_roundtrips_without_inference(tmp_path: Path):
    card = SceneCard(
        "photo.jpg", 10, 10, ["#112233"], .5, .5, "landscape", "MOMENT",
        metadata=SourceMetadata(date="2026-08-10", location="Harbor Road", catalogue_id="SCS-001"),
    )
    story = tmp_path / "story.json"
    save_cards([card], story)
    loaded = load_cards(story, resolve_sources=False)[0]
    assert loaded.metadata.date == "2026-08-10"
    assert loaded.metadata.location == "Harbor Road"
    assert loaded.metadata.collection == ""
