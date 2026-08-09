from __future__ import annotations

from html import escape
from pathlib import Path

from .model import SceneCard


PAPER = "#F3F0E8"
INK = "#202321"


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
             f'<text x="{margin}" y="80" font-family="ui-monospace,monospace" font-size="18" letter-spacing="4" fill="{accent}">MOMENTS TO PAGES</text>',
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
