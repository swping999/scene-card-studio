from __future__ import annotations

import argparse
from pathlib import Path

from .analyze import analyze_image, assign_story_roles
from .model import load_cards, save_cards
from .director import recommend_systems
from .render import render_png, render_svg


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="scene-card-studio")
    commands = root.add_subparsers(dest="command", required=True)
    analyze = commands.add_parser("analyze", help="Create Scene Cards from photos")
    analyze.add_argument("photos", nargs="+")
    analyze.add_argument("-o", "--output", default="story.json")
    analyze.add_argument("--reorder", action="store_true", help="Allow heuristic reordering; input order is preserved by default")
    render = commands.add_parser("render", help="Render Scene Cards to editable SVG")
    render.add_argument("story")
    render.add_argument("-o", "--output")
    render.add_argument("--style", choices=["source-contact-sheet", "editorial-sequence", "family-archive", "memory-atlas", "field-log", "editorial-minimal", "memory-map", "field-notes"], default="editorial-sequence")
    render.add_argument("--embed-images", action="store_true")
    render.add_argument("--format", choices=["svg", "png"], default="svg")
    render.add_argument("--mode", choices=["presentation", "workprint"], default="presentation")
    recommend = commands.add_parser("recommend", help="Recommend Narrative Systems with reasons")
    recommend.add_argument("story")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "analyze":
        save_cards(assign_story_roles([analyze_image(Path(value)) for value in args.photos], reorder=args.reorder), Path(args.output))
    elif args.command == "recommend":
        for item in recommend_systems(load_cards(Path(args.story))):
            print(f"{item.system}\t{item.score:.2f}\t{item.reason}")
    elif args.command == "render":
        story_path = Path(args.story)
        output = Path(args.output) if args.output else Path(f"story.{args.format}")
        if output.suffix.lower() != f".{args.format}":
            raise SystemExit(f"Output extension must be .{args.format} for --format {args.format}")
        cards = load_cards(story_path)
        if args.format == "png":
            render_png(cards, output, args.style, args.mode)
        else:
            render_svg(cards, output, args.style, args.embed_images, args.mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
