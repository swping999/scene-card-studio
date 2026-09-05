import re
from pathlib import Path

from moments_to_pages.expression_profiles import EXPRESSION_PROFILES
from moments_to_pages.narrative_systems import SUPPORTED_SYSTEMS


ROOT = Path(__file__).resolve().parents[1]
GUIDES = (ROOT / "VISUAL-GUIDE.md", ROOT / "VISUAL-GUIDE.zh-CN.md")


def _public_profile_names() -> set[str]:
    return {
        profile
        for profiles in EXPRESSION_PROFILES.values()
        for profile in profiles
        if profile != "full-watercolor-memory"
    }


def test_visual_guides_cover_every_system_and_profile():
    profiles = _public_profile_names()
    assert len(SUPPORTED_SYSTEMS) == 11
    assert len(profiles) == 24

    for guide in GUIDES:
        text = guide.read_text()
        for system in SUPPORTED_SYSTEMS:
            assert f"`{system}`" in text, f"{guide.name} omits Narrative System {system}"
        for profile in profiles:
            assert f"`{profile}`" in text, f"{guide.name} omits Expression Profile {profile}"


def test_visual_guide_examples_exist_and_readmes_link_the_guides():
    image_pattern = re.compile(r'<img src="([^"]+)"')
    for guide in GUIDES:
        image_paths = image_pattern.findall(guide.read_text())
        assert len(image_paths) >= 35
        for image_path in image_paths:
            assert (ROOT / image_path).is_file(), f"{guide.name} references missing {image_path}"

    assert "[Visual Selection Guide](VISUAL-GUIDE.md)" in (ROOT / "README.md").read_text()
    assert "[视觉选择指南](VISUAL-GUIDE.zh-CN.md)" in (ROOT / "README.zh-CN.md").read_text()
