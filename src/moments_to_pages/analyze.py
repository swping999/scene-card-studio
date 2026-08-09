from __future__ import annotations

from pathlib import Path
import colorsys

from .model import Direction, Observation, SceneCard


def _hex(rgb: tuple[int, int, int]) -> str:
    return "#%02X%02X%02X" % rgb


def analyze_image(path: Path) -> SceneCard:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Photo analysis requires Pillow: pip install 'moments-to-pages[images]'") from exc

    with Image.open(path) as image:
        image = image.convert("RGB")
        width, height = image.size
        sample = image.copy()
        sample.thumbnail((160, 160))
        quantized = sample.quantize(colors=5, method=2).convert("RGB")
        colors = quantized.getcolors(160 * 160) or []
        ranked = sorted(colors, reverse=True)
        palette = [_hex(rgb) for _, rgb in ranked[:5]]
        pixels = list(sample.getdata())

    hsv = [colorsys.rgb_to_hsv(r / 255, g / 255, b / 255) for r, g, b in pixels]
    brightness = round(sum(v for _, _, v in hsv) / len(hsv), 3)
    saturation = round(sum(s for _, s, _ in hsv) / len(hsv), 3)
    orientation = "landscape" if width > height else "portrait" if height > width else "square"
    return SceneCard(
        source=str(path), width=width, height=height, palette=palette,
        brightness=brightness, saturation=saturation, orientation=orientation,
        caption=path.stem.replace("-", " ").replace("_", " ").upper()[:42] or "UNTITLED MOMENT",
        observation=Observation(),
        direction=Direction(
            emotional_tone=["quiet", "luminous"] if brightness > .58 else ["reflective", "intimate"],
            confidence=.55,
        ),
    )


def assign_story_roles(cards: list[SceneCard]) -> list[SceneCard]:
    if not cards:
        return cards
    ordered = sorted(cards, key=lambda card: (card.brightness, card.saturation))
    roles = ["opening", "development", "pause", "closing"]
    for index, card in enumerate(ordered):
        card.direction.story_role = roles[min(index * len(roles) // len(ordered), len(roles) - 1)]
    return ordered
