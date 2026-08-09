from __future__ import annotations

import argparse
from pathlib import Path

from .analyze import analyze_image, assign_story_roles
from .model import load_cards, save_cards
from .render import render_svg


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="moments-to-pages")
    commands = root.add_subparsers(dest="command", required=True)
    analyze = commands.add_parser("analyze", help="Create Scene Cards from photos")
    analyze.add_argument("photos", nargs="+")
    analyze.add_argument("-o", "--output", default="story.json")
    render = commands.add_parser("render", help="Render Scene Cards to editable SVG")
    render.add_argument("story")
    render.add_argument("-o", "--output", default="story.svg")
    render.add_argument("--style", choices=["editorial-minimal", "memory-map", "field-notes"], default="editorial-minimal")
    render.add_argument("--embed-images", action="store_true")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "analyze":
        save_cards(assign_story_roles([analyze_image(Path(value)) for value in args.photos]), Path(args.output))
    else:
        render_svg(load_cards(Path(args.story)), Path(args.output), args.style, args.embed_images)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
