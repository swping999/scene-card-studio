from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .analyze import analyze_image, assign_story_roles
from .model import load_cards, save_cards
from .director import recommend_systems
from .prompt_compiler import SUPPORTED_SYSTEMS, compile_manifest
from .privacy import build_upload_consent
from .render import render_png, render_svg
from .review import bind_outputs, build_retry_manifest, file_sha256


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
    render.add_argument("--allow-external-sources", action="store_true", help="Allow embedded source images outside the current working directory")
    render.add_argument("--format", choices=["svg", "png"], default="svg")
    render.add_argument("--mode", choices=["presentation", "workprint"], default="presentation")
    recommend = commands.add_parser("recommend", help="Recommend Narrative Systems with reasons")
    recommend.add_argument("story")
    compile_cmd = commands.add_parser("compile", help="Compile Scene Cards into versioned image-generation prompts")
    compile_cmd.add_argument("story")
    compile_cmd.add_argument("--system", choices=SUPPORTED_SYSTEMS, required=True)
    compile_cmd.add_argument("--expression-profile", default="source-led", help="Replaceable visual expression profile; defaults to source-led")
    compile_cmd.add_argument("--aspect-ratio", default="source", help="source, 3:2, 2:3, 4:5, 1:1, or another target ratio")
    compile_cmd.add_argument("--reference-output", action="append", default=[], help="Optional benchmark output path; repeat in prompt order")
    compile_cmd.add_argument("-o", "--output", default="prompt-manifest.json")
    retry = commands.add_parser("retry", help="Build targeted retry prompts from an aesthetic assessment")
    retry.add_argument("manifest")
    retry.add_argument("assessment")
    retry.add_argument("-o", "--output", default="retry-manifest.json")
    bind = commands.add_parser("bind-outputs", help="Bind generated output files and hashes to prompt ids before review")
    bind.add_argument("manifest")
    bind.add_argument("--result", action="append", required=True, help="PROMPT_ID=OUTPUT_PATH; repeat for every prompt")
    bind.add_argument("-o", "--output", default="render-manifest.json")
    consent = commands.add_parser("consent", help="Record explicit consent for uploading the manifest's exact source files")
    consent.add_argument("manifest")
    consent.add_argument("--provider", required=True)
    consent.add_argument("--purpose", required=True)
    consent.add_argument("--confirm", action="store_true", help="Confirm that the user explicitly approved this provider, purpose, and file list")
    consent.add_argument("-o", "--output", default="upload-consent.json")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "analyze":
        output = Path(args.output)
        cards = assign_story_roles([analyze_image(Path(value).resolve()) for value in args.photos], reorder=args.reorder)
        output_base = output.resolve().parent
        for card in cards:
            card.source = Path(os.path.relpath(Path(card.source).resolve(), output_base)).as_posix()
        save_cards(cards, output)
    elif args.command == "recommend":
        for item in recommend_systems(load_cards(Path(args.story))):
            print(f"{item.system}\t{item.score:.2f}\t{item.reason}")
    elif args.command == "compile":
        story_path = Path(args.story)
        manifest = compile_manifest(
            load_cards(story_path, resolve_sources=False),
            args.system,
            aspect_ratio=args.aspect_ratio,
            expression_profile=args.expression_profile,
            source_root=story_path.resolve().parent,
            story_path=str(story_path),
            reference_outputs=args.reference_output,
        )
        Path(args.output).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    elif args.command == "retry":
        manifest_path = Path(args.manifest)
        manifest = json.loads(manifest_path.read_text())
        assessment = json.loads(Path(args.assessment).read_text())
        retry_manifest = build_retry_manifest(manifest, assessment, manifest_sha256=file_sha256(manifest_path))
        Path(args.output).write_text(json.dumps(retry_manifest, ensure_ascii=False, indent=2) + "\n")
    elif args.command == "bind-outputs":
        bindings = {}
        for value in args.result:
            if "=" not in value:
                raise SystemExit("--result must use PROMPT_ID=OUTPUT_PATH")
            prompt_id, path = value.split("=", 1)
            if not prompt_id or not path:
                raise SystemExit("--result must use PROMPT_ID=OUTPUT_PATH")
            bindings[prompt_id] = path
        manifest = json.loads(Path(args.manifest).read_text())
        bound = bind_outputs(manifest, bindings, base=Path.cwd())
        Path(args.output).write_text(json.dumps(bound, ensure_ascii=False, indent=2) + "\n")
    elif args.command == "consent":
        manifest_path = Path(args.manifest)
        manifest = json.loads(manifest_path.read_text())
        record = build_upload_consent(
            manifest,
            manifest_sha256=file_sha256(manifest_path),
            provider=args.provider,
            purpose=args.purpose,
            user_confirmed=args.confirm,
        )
        Path(args.output).write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    elif args.command == "render":
        story_path = Path(args.story)
        output = Path(args.output) if args.output else Path(f"story.{args.format}")
        if output.suffix.lower() != f".{args.format}":
            raise SystemExit(f"Output extension must be .{args.format} for --format {args.format}")
        cards = load_cards(story_path)
        if args.format == "png":
            render_png(cards, output, args.style, args.mode)
        else:
            render_svg(
                cards,
                output,
                args.style,
                args.embed_images,
                args.mode,
                allowed_source_root=Path.cwd().resolve(),
                allow_external_sources=args.allow_external_sources,
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
