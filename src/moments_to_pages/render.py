from __future__ import annotations

from html import escape
from pathlib import Path
from urllib.parse import quote
import os
import re

from .model import SceneCard


PAPER = "#F3F0E8"
INK = "#202321"


def _load_font(ImageFont, size: int, mono: bool = False):
    candidates = ([
        str(Path(__file__).resolve().parent / "assets/fonts/NotoSansMono-Regular.ttf"),
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ] if mono else [
        str(Path(__file__).resolve().parent / "assets/fonts/NotoSansCJKsc-Regular.otf"),
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ])
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _image_href(card: SceneCard, embed: bool, output: Path) -> str:
    path = Path(card.source)
    if not embed:
        relative = os.path.relpath(path.resolve(), output.resolve().parent)
        return quote(Path(relative).as_posix(), safe="/.-_~")
    import base64, mimetypes
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def _safe_color(value: str, fallback: str = "#275D78") -> str:
    return value if re.fullmatch(r"#[0-9A-Fa-f]{6}", value or "") else fallback


def render_svg(cards: list[SceneCard], output: Path, style: str = "editorial-sequence", embed: bool = False, mode: str = "presentation") -> None:
    if not cards:
        raise ValueError("At least one Scene Card is required")
    aliases = {"editorial-minimal": "editorial-sequence", "memory-map": "memory-atlas", "field-notes": "field-log"}
    style = aliases.get(style, style)
    width = 1200
    if style == "field-log":
        height = max(1000, 260 + len(cards) * 390)
    elif style in {"source-contact-sheet", "family-archive"}:
        height = max(1000, 260 + ((len(cards) + 1) // 2) * 570)
    elif style == "editorial-sequence":
        height = max(1200, 980 + ((max(0, len(cards) - 1) + 1) // 2) * 500)
    else:
        height = max(1400, 520 + len(cards) * 260)
    margin = 72
    accent = _safe_color(cards[0].palette[0] if cards[0].palette else "#275D78")
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             f'<rect width="100%" height="100%" fill="{PAPER}"/>',
             f'<text x="{margin}" y="80" font-family="ui-monospace,monospace" font-size="18" letter-spacing="4" fill="{accent}">SCENE CARD STUDIO</text>',
             f'<text x="{margin}" y="145" font-family="system-ui,sans-serif" font-size="54" fill="{INK}">{escape(style.replace("-", " ").upper())}</text>']

    def image(card: SceneCard, x: int, y: int, w: int, h: int) -> None:
        parts.append(f'<image href="{escape(_image_href(card, embed, output))}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>')

    if style == "editorial-sequence":
        image(cards[0], 72, 220, 1056, 580)
        parts.append(f'<rect x="72" y="710" width="1056" height="90" fill="{INK}"/>')
        parts.append(f'<text x="96" y="768" font-family="system-ui,sans-serif" font-size="28" fill="#FFFFFF">{escape(cards[0].caption)}</text>')
        for i, card in enumerate(cards[1:]):
            x, y = 72 + (i % 2) * 540, 900 + (i // 2) * 500
            image(card, x, y, 516, 340)
            parts.append(f'<text x="{x}" y="{y+390}" font-family="system-ui,sans-serif" font-size="24" fill="{INK}">{escape(card.caption[:42])}</text>')
    elif style == "field-log":
        parts.append('<line x1="500" y1="220" x2="500" y2="95%" stroke="#B8B2A7" stroke-width="2"/>')
        for i, card in enumerate(cards):
            y = 220 + i * 390
            image(card, 72, y, 380, 285)
            subjects = ", ".join(card.observation.subjects[:3])
            parts.extend([
                f'<text x="540" y="{y+25}" font-family="ui-monospace,monospace" font-size="15" fill="{accent}">FIELD NOTE / {i+1:02d}</text>',
                f'<text x="540" y="{y+75}" font-family="system-ui,sans-serif" font-size="26" fill="{INK}">{escape(card.caption[:38])}</text>',
                f'<text x="540" y="{y+135}" font-family="ui-monospace,monospace" font-size="14" fill="#666762">SUBJECTS  {escape(subjects[:52])}</text>',
                f'<text x="540" y="{y+180}" font-family="ui-monospace,monospace" font-size="14" fill="#666762">GESTURE   {escape(card.observation.dominant_gesture[:50])}</text>'])
    elif style == "family-archive":
        for i, card in enumerate(cards):
            x, y = 72 + (i % 2) * 540, 230 + (i // 2) * 570 + (35 if i % 2 else 0)
            parts.append(f'<rect x="{x-10}" y="{y-10}" width="536" height="470" fill="#DED3BF"/>')
            image(card, x, y, 516, 390)
            parts.append(f'<text x="{x+14}" y="{y+430}" font-family="ui-monospace,monospace" font-size="15" fill="#A0664B">ARCHIVE {i+1:02d} · {escape(card.caption[:32])}</text>')
    elif style == "memory-atlas":
        map_path = Path(__file__).resolve().parent / "assets/maps/coastal-memory-atlas.png"
        map_href = quote(Path(os.path.relpath(map_path, output.resolve().parent)).as_posix(), safe="/.-_~")
        parts.append(f'<image href="{escape(map_href)}" x="72" y="220" width="720" height="{height-310}" preserveAspectRatio="xMidYMid slice"/>')
        for i, card in enumerate(cards):
            y = 240 + i * 250
            image(card, 840, y, 288, 170)
            parts.append(f'<text x="840" y="{y+205}" font-family="ui-monospace,monospace" font-size="14" fill="#755D45">PLACE {i+1:02d} · {escape(card.caption[:26])}</text>')
    else:
        for i, card in enumerate(cards):
            x, y = 72 + (i % 2) * 540, 220 + (i // 2) * 570
            image(card, x, y, 516, 390)
            parts.append(f'<text x="{x}" y="{y+430}" font-family="system-ui,sans-serif" font-size="24" fill="{INK}">{escape(Path(card.source).stem[:36])}</text>')
    if mode == "workprint":
        parts.append(f'<text x="72" y="{height-50}" font-family="ui-monospace,monospace" font-size="14" fill="#666762">WORKPRINT · OBSERVATION / INTERPRETATION / DIRECTION</text>')
    parts.append('</svg>')
    output.write_text("\n".join(parts) + "\n")


def render_png(cards: list[SceneCard], output: Path, system: str = "editorial-sequence", mode: str = "presentation") -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:
        raise RuntimeError("PNG rendering requires Pillow: pip install 'scene-card-studio[images]'") from exc
    aliases = {"editorial-minimal": "editorial-sequence", "memory-map": "memory-atlas", "field-notes": "field-log"}
    system = aliases.get(system, system)
    if not cards:
        raise ValueError("At least one Scene Card is required")
    if system == "source-contact-sheet":
        canvas_h = max(1000, 240 + ((len(cards) + 1) // 2) * 700)
    elif system == "field-log":
        canvas_h = max(1000, 300 + len(cards) * 440)
    elif system == "family-archive":
        canvas_h = max(1500, 500 + ((len(cards) + 1) // 2) * 620)
    elif system == "editorial-sequence":
        canvas_h = max(1500, 1000 + ((max(0, len(cards) - 1) + 1) // 2) * 560)
    else:
        canvas_h = max(1800, 500 + len(cards) * 260)
    canvas = Image.new("RGB", (1200, canvas_h), PAPER)
    draw = ImageDraw.Draw(canvas)
    title_font = _load_font(ImageFont, 52)
    body_font = _load_font(ImageFont, 24)
    meta_font = _load_font(ImageFont, 15, mono=True)
    accent = _safe_color(cards[0].palette[0] if cards[0].palette else "#275D78")

    def fit_text(value: str, font, max_width: int) -> str:
        if draw.textlength(value, font=font) <= max_width:
            return value
        shortened = value
        while shortened and draw.textlength(shortened + "…", font=font) > max_width:
            shortened = shortened[:-1]
        return shortened.rstrip() + "…"

    draw.text((72, 55), "SCENE CARD STUDIO", fill=accent, font=meta_font)
    draw.text((72, 105), system.replace("-", " ").upper(), fill=INK, font=title_font)
    if mode == "workprint":
        draw.text((72, 172), "OBSERVATION → INTERPRETATION → DIRECTION → NARRATIVE SYSTEM", fill="#666762", font=meta_font)

    def paste_photo(card: SceneCard, box: tuple[int, int, int, int]) -> None:
        x, y, width, height = box
        with Image.open(card.source) as opened:
            source = ImageOps.exif_transpose(opened)
            if source.mode in {"RGBA", "LA"} or "transparency" in source.info:
                rgba = source.convert("RGBA")
                background = Image.new("RGBA", rgba.size, PAPER)
                background.alpha_composite(rgba)
                source = background.convert("RGB")
            else:
                source = source.convert("RGB")
            photo = ImageOps.fit(source, (width, height), method=Image.Resampling.LANCZOS)
        canvas.paste(photo, (x, y))

    if system == "source-contact-sheet":
        for index, card in enumerate(cards):
            x = 72 + (index % 2) * 540
            y = 240 + (index // 2) * 700
            paste_photo(card, (x, y, 516, 420))
            draw.text((x, y + 450), f"SOURCE {index + 1:02d} · UNINTERPRETED", fill=accent, font=meta_font)
            label = fit_text(Path(card.source).stem.replace("-", " ").upper(), body_font, 516)
            draw.text((x, y + 485), label, fill=INK, font=body_font)
            draw.text((x, y + 532), "Original input before sequencing or visual direction.", fill="#666762", font=meta_font)
            draw.line((x, y + 570, x + 516, y + 570), fill="#C8C4BA", width=1)

    elif system == "editorial-sequence":
        hero = cards[0]
        paste_photo(hero, (72, 240, 1056, 610))
        draw.rectangle((72, 760, 1128, 850), fill=(20, 26, 25))
        draw.text((96, 780), "01 · OPENING" if mode == "workprint" else "01", fill="#E8E2D5", font=meta_font)
        draw.text((96, 812), fit_text(hero.caption, body_font, 900), fill="#FFFFFF", font=body_font)
        for offset, card in enumerate(cards[1:]):
            x = 72 + offset * 540
            x = 72 + (offset % 2) * 540
            y = 930 + (offset // 2) * 560
            paste_photo(card, (x, y, 516, 400))
            label = f"0{offset + 2} · {card.story_role.upper()}" if mode == "workprint" else f"0{offset + 2}"
            draw.text((x, y + 430), label, fill=accent, font=meta_font)
            draw.text((x, y + 465), fit_text(card.caption, body_font, 516), fill=INK, font=body_font)
            if mode == "workprint":
                draw.text((x, y + 515), fit_text(card.direction.director_note, meta_font, 516), fill="#666762", font=meta_font)
        draw.text((72, canvas_h - 80), "CARE → PAUSE → DEPARTURE", fill=accent, font=meta_font)

    elif system == "memory-atlas":
        map_path = Path(__file__).resolve().parent / "assets/maps/coastal-memory-atlas.png"
        with Image.open(map_path).convert("RGB") as source:
            memory_map = ImageOps.fit(source, (760, 1260), method=Image.Resampling.LANCZOS)
        canvas.paste(memory_map, (72, 240))
        draw.rectangle((856, 240, 1128, canvas_h - 300), fill="#E8E1D2")
        draw.text((884, 275), "PLACES HELD", fill="#755D45", font=meta_font)
        for index, card in enumerate(cards[:3]):
            y = 330 + index * 260
            paste_photo(card, (884, y, 216, 150))
            label = f"0{index + 1} / {card.story_role.upper()}" if mode == "workprint" else f"PLACE 0{index + 1}"
            draw.text((884, y + 175), label, fill="#755D45", font=meta_font)
            draw.text((884, y + 205), fit_text(card.caption, meta_font, 216), fill=INK, font=meta_font)
            draw.text((884, y + 245), fit_text(card.interpretation.narrative_intent, meta_font, 216), fill="#666762", font=meta_font)
        draw.text((72, canvas_h - 220), "A SPATIAL MEMORY, NOT A LITERAL ROUTE.", fill="#755D45", font=meta_font)

    elif system == "field-log":
        draw.line((510, 240, 510, 1570), fill="#B8B2A7", width=2)
        for index, card in enumerate(cards[:3]):
            y = 240 + index * 440
            paste_photo(card, (72, y, 390, 300))
            draw.text((550, y), f"FIELD NOTE / 0{index + 1}", fill=accent, font=meta_font)
            draw.text((550, y + 45), fit_text(card.caption, body_font, 550), fill=INK, font=body_font)
            subjects = ", ".join(card.observation.subjects[:3]) or "unclassified subject"
            lines = [
                ("SUBJECTS", subjects),
                ("GESTURE", card.observation.dominant_gesture),
                ("QUIET REGION", ", ".join(card.observation.quiet_regions)),
            ]
            if mode == "workprint":
                lines.append(("READING", card.interpretation.narrative_intent))
            for row, (label, value) in enumerate(lines):
                yy = y + 105 + row * 48
                draw.text((550, yy), label, fill="#777872", font=meta_font)
                draw.text((700, yy), fit_text(value, meta_font, 400), fill=INK, font=meta_font)
            draw.line((550, y + 300, 1128, y + 300), fill="#C8C4BA", width=1)

    elif system == "family-archive":
        archive = "#A0664B"
        placements = []
        for index in range(len(cards)):
            row, col = divmod(index, 2)
            placements.append((72 + col * 540, 260 + row * 620 + (38 if col else 0), 516, 470))
        for index, (card, box) in enumerate(zip(cards, placements)):
            x, y, width, height = box
            draw.rectangle((x - 12, y - 12, x + width + 12, y + height + 58), fill="#DED3BF")
            paste_photo(card, box)
            label = f"ARCHIVE 0{index + 1} · {card.story_role.upper()}" if mode == "workprint" else f"ARCHIVE 0{index + 1}"
            draw.text((x + 14, y + height + 18), label, fill=archive, font=meta_font)
        draw.text((72, canvas_h - 170), "REPEATED GESTURES BECOME A FAMILY RECORD.", fill=archive, font=body_font)
        draw.text((72, canvas_h - 115), "Laundry / shared work / photographs kept and returned to.", fill="#666762", font=meta_font)
        draw.line((72, canvas_h - 55, 1128, canvas_h - 55), fill=archive, width=3)

    canvas.save(output, optimize=True)
