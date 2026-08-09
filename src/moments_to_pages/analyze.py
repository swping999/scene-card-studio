from __future__ import annotations

from pathlib import Path
import colorsys

from .model import Direction, Interpretation, Observation, SceneCard


def _hex(rgb: tuple[int, int, int]) -> str:
    return "#%02X%02X%02X" % rgb


def analyze_image(path: Path) -> SceneCard:
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise RuntimeError("Photo analysis requires Pillow: pip install 'scene-card-studio[images]'") from exc

    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode in {"RGBA", "LA"} or "transparency" in image.info:
            rgba = image.convert("RGBA")
            background = Image.new("RGBA", rgba.size, "white")
            background.alpha_composite(rgba)
            image = background.convert("RGB")
        else:
            image = image.convert("RGB")
        width, height = image.size
        sample = image.copy()
        sample.thumbnail((160, 160))
        quantized = sample.quantize(colors=5, method=2).convert("RGB")
        colors = quantized.getcolors(160 * 160) or []
        ranked = sorted(colors, reverse=True)
        palette = [_hex(rgb) for _, rgb in ranked[:5]]
        pixel_data = sample.get_flattened_data() if hasattr(sample, "get_flattened_data") else sample.getdata()
        pixels = list(pixel_data)

    hsv = [colorsys.rgb_to_hsv(r / 255, g / 255, b / 255) for r, g, b in pixels]
    brightness = round(sum(v for _, _, v in hsv) / len(hsv), 3)
    saturation = round(sum(s for _, s, _ in hsv) / len(hsv), 3)
    orientation = "landscape" if width > height else "portrait" if height > width else "square"
    return SceneCard(
        source=str(path), width=width, height=height, palette=palette,
        brightness=brightness, saturation=saturation, orientation=orientation,
        caption=path.stem.replace("-", " ").replace("_", " ").upper()[:42] or "UNTITLED MOMENT",
        observation=Observation(),
        interpretation=Interpretation(
            emotional_tone=["quiet", "luminous"] if brightness > .58 else ["reflective", "intimate"],
            confidence=.35,
            method="heuristic",
        ),
        direction=Direction(),
    )


def assign_story_roles(cards: list[SceneCard], reorder: bool = False) -> list[SceneCard]:
    if not cards:
        return cards
    ordered = sorted(cards, key=lambda card: (card.brightness, card.saturation)) if reorder else list(cards)
    role_sets = {
        1: ["opening"],
        2: ["opening", "closing"],
        3: ["opening", "development", "closing"],
    }
    roles = role_sets.get(len(ordered), ["opening", "development", "pause", "closing"])
    for index, card in enumerate(ordered):
        card.direction.story_role = roles[index] if len(ordered) <= 3 else roles[min(index * len(roles) // len(ordered), len(roles) - 1)]
    return ordered
