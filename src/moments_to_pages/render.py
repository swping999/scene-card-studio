from __future__ import annotations

from html import escape
from pathlib import Path

from .model import SceneCard


PAPER = "#F3F0E8"
INK = "#202321"


def _load_font(ImageFont, size: int, mono: bool = False):
    candidates = ([
        "assets/fonts/NotoSansMono-Regular.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ] if mono else [
        "assets/fonts/NotoSans-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ])
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _image_href(card: SceneCard, embed: bool) -> str:
    path = Path(card.source)
    if not embed:
        return path.as_uri() if path.is_absolute() else path.as_posix()
    import base64, mimetypes
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def render_svg(cards: list[SceneCard], output: Path, style: str = "editorial-minimal", embed: bool = False) -> None:
    if not cards:
        raise ValueError("At least one Scene Card is required")
    width, height = 1200, 1800
    margin, gap = 72, 24
    columns = 2 if len(cards) > 1 else 1
    rows = (len(cards) + columns - 1) // columns
    cell_w = (width - margin * 2 - gap * (columns - 1)) / columns
    cell_h = (height - 260 - gap * (rows - 1)) / rows
    accent = cards[0].palette[0] if cards[0].palette else "#275D78"
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             f'<rect width="100%" height="100%" fill="{PAPER}"/>',
             f'<text x="{margin}" y="80" font-family="ui-monospace,monospace" font-size="18" letter-spacing="4" fill="{accent}">SCENE CARD STUDIO</text>',
             f'<text x="{margin}" y="145" font-family="system-ui,sans-serif" font-size="54" fill="{INK}">A visual story in {len(cards)} frame(s)</text>']
    for i, card in enumerate(cards):
        col, row = i % columns, i // columns
        x, y = margin + col * (cell_w + gap), 220 + row * (cell_h + gap)
        photo_h = cell_h * (0.68 if style == "editorial-minimal" else 0.58)
        color = card.palette[(i + 1) % len(card.palette)] if card.palette else accent
        if style == "memory-map":
            parts.append(f'<path d="M{x} {y+photo_h*.8} C{x+cell_w*.3} {y-photo_h*.1}, {x+cell_w*.7} {y+photo_h*1.1}, {x+cell_w} {y+photo_h*.25}" fill="none" stroke="{color}" stroke-width="18" opacity=".85"/>')
        parts.append(f'<image href="{escape(_image_href(card, embed))}" x="{x}" y="{y}" width="{cell_w}" height="{photo_h}" preserveAspectRatio="xMidYMid slice"/>')
        if style == "field-notes":
            parts.append(f'<rect x="{x+cell_w*.72}" y="{y+photo_h-24}" width="{cell_w*.25}" height="48" fill="{color}"/>')
        parts.extend([
            f'<text x="{x}" y="{y+photo_h+42}" font-family="ui-monospace,monospace" font-size="14" letter-spacing="2" fill="{color}">{i+1:02d} · {escape(card.story_role.upper())}</text>',
            f'<text x="{x}" y="{y+photo_h+82}" font-family="system-ui,sans-serif" font-size="26" fill="{INK}">{escape(card.caption)}</text>',
            f'<line x1="{x}" y1="{y+photo_h+108}" x2="{x+cell_w}" y2="{y+photo_h+108}" stroke="{INK}" opacity=".2"/>'])
    parts.append('</svg>')
    output.write_text("\n".join(parts) + "\n")


def render_png(cards: list[SceneCard], output: Path, system: str = "editorial-sequence") -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:
        raise RuntimeError("PNG rendering requires Pillow: pip install 'scene-card-studio[images]'") from exc
    aliases = {"editorial-minimal": "editorial-sequence", "memory-map": "memory-atlas", "field-notes": "field-log"}
    system = aliases.get(system, system)
    canvas = Image.new("RGB", (1200, 1800), PAPER)
    draw = ImageDraw.Draw(canvas)
    title_font = _load_font(ImageFont, 52)
    body_font = _load_font(ImageFont, 24)
    meta_font = _load_font(ImageFont, 15, mono=True)
    accent = cards[0].palette[0] if cards and cards[0].palette else "#275D78"

    def fit_text(value: str, font, max_width: int) -> str:
        if draw.textlength(value, font=font) <= max_width:
            return value
        shortened = value
        while shortened and draw.textlength(shortened + "…", font=font) > max_width:
            shortened = shortened[:-1]
        return shortened.rstrip() + "…"

    draw.text((72, 55), "SCENE CARD STUDIO", fill=accent, font=meta_font)
    draw.text((72, 105), system.replace("-", " ").upper(), fill=INK, font=title_font)
    draw.text((72, 172), "OBSERVATION → INTERPRETATION → DIRECTION → NARRATIVE SYSTEM", fill="#666762", font=meta_font)
    columns, margin, gap = 2, 72, 24
    cell_w, cell_h = 516, 700
    route_points: list[tuple[int, int]] = []
    for index, card in enumerate(cards):
        x = margin + (index % columns) * (cell_w + gap)
        y = 240 + (index // columns) * (cell_h + gap)
        photo_h = 420 if system in {"editorial-sequence", "source-contact-sheet"} else 360
        with Image.open(card.source).convert("RGB") as source:
            photo = ImageOps.fit(source, (cell_w, photo_h), method=Image.Resampling.LANCZOS)
        canvas.paste(photo, (x, y))
        if system == "family-archive":
            draw.rectangle((x, y + photo_h - 12, x + cell_w, y + photo_h), fill="#A0664B")
            draw.text((x + 16, y + 16), f"ARCHIVE / {index + 1:02d}", fill=PAPER, font=meta_font)
        if system == "field-log":
            draw.rectangle((x + cell_w - 130, y + photo_h - 18, x + cell_w - 12, y + photo_h + 22), fill=accent)
        if system == "source-contact-sheet":
            draw.text((x, y + photo_h + 30), f"SOURCE {index + 1:02d} · UNINTERPRETED", fill=accent, font=meta_font)
            label = fit_text(Path(card.source).stem.replace("-", " ").upper(), body_font, cell_w)
            draw.text((x, y + photo_h + 65), label, fill=INK, font=body_font)
            note = "Original input before sequencing or visual direction."
        elif system == "field-log":
            draw.text((x, y + photo_h + 30), f"FIELD NOTE {index + 1:02d} · OBSERVATION", fill=accent, font=meta_font)
            draw.text((x, y + photo_h + 65), fit_text(card.caption, body_font, cell_w), fill=INK, font=body_font)
            subjects = ", ".join(card.observation.subjects[:3]) or "unclassified subject"
            note = f"Seen: {subjects} · gesture: {card.observation.dominant_gesture}"[:82]
        elif system == "family-archive":
            draw.text((x, y + photo_h + 30), f"{index + 1:02d} · FAMILY RECORD · {card.story_role.upper()}", fill="#A0664B", font=meta_font)
            draw.text((x, y + photo_h + 65), fit_text(card.caption, body_font, cell_w), fill=INK, font=body_font)
            note = f"Kept as: {card.interpretation.narrative_intent} · {card.direction.director_note}"[:82]
        else:
            draw.text((x, y + photo_h + 30), f"{index + 1:02d} · {card.story_role.upper()}", fill=accent, font=meta_font)
            draw.text((x, y + photo_h + 65), fit_text(card.caption, body_font, cell_w), fill=INK, font=body_font)
            note = card.direction.director_note[:64]
        draw.text((x, y + photo_h + 112), fit_text(note, meta_font, cell_w), fill="#666762", font=meta_font)
        draw.line((x, y + photo_h + 150, x + cell_w, y + photo_h + 150), fill="#C8C4BA", width=1)
        route_points.append((x + cell_w - 24 if index % 2 == 0 else x + 24, y + photo_h - 24))
    if system == "memory-atlas" and len(route_points) > 1:
        draw.line(route_points, fill=accent, width=7, joint="curve")
        for number, point in enumerate(route_points, 1):
            px, py = point
            draw.ellipse((px - 13, py - 13, px + 13, py + 13), fill=PAPER, outline=accent, width=5)
            draw.text((px + 18, py - 13), f"{number:02d}", fill=accent, font=meta_font)
    if system == "family-archive":
        draw.line((72, 1740, 1128, 1740), fill="#A0664B", width=3)
        draw.text((72, 1752), "A FAMILY IS REMEMBERED THROUGH REPEATED GESTURES.", fill="#A0664B", font=meta_font)
    canvas.save(output, optimize=True)
