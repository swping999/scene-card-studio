# Moments to Pages

Turn 1–12 personal photos into a structured visual story instead of applying one more photo filter.

Moments to Pages separates observation from rendering. Each photo becomes a portable Scene Card, then one of several deterministic layout systems turns those cards into an editable SVG. The same story data can later drive a social carousel, printable micro-zine, PDF, or website.

## Why this project

Most photo-to-poster tools lock analysis, prompting, style, and output into one opaque operation. This project keeps the intermediate narrative decisions visible and editable:

```text
photos → Scene Cards → story order → visual system → editable output
```

The initial release includes three original systems:

- `editorial-minimal`: spacious photo essay;
- `memory-map`: route and movement-led composition;
- `field-notes`: documentary observation sheet.

## Generated showcase

The repository includes three original AI-generated source photographs and the
Scene Cards produced from them. No personal photographs or third-party style
assets are included.

| Editorial Minimal | Memory Map | Field Notes |
| --- | --- | --- |
| [Open editable SVG](examples/outputs/editorial-minimal.svg) | [Open editable SVG](examples/outputs/memory-map.svg) | [Open editable SVG](examples/outputs/field-notes.svg) |

Source photographs are under [`examples/photos`](examples/photos), and the
machine-readable narrative is [`examples/generated-story.json`](examples/generated-story.json).

## Quick start

Requires Python 3.10 or newer. Automatic image analysis uses Pillow.

```bash
python -m pip install -e '.[images]'
moments-to-pages analyze photos/*.jpg --output story.json
moments-to-pages render story.json --style editorial-minimal --output story.svg
```

Open `story.json` to revise captions, subjects, ordering, or colors, then render again. Add `--embed-images` for a self-contained SVG.

Rendering an existing Scene Card file has no third-party dependencies:

```bash
PYTHONPATH=src python -m moments_to_pages.cli render examples/story.json -o story.svg
```

## Scene Card

```json
{
  "source": "photos/harbor.jpg",
  "width": 1600,
  "height": 1067,
  "palette": ["#23383D", "#D66549", "#D9D0B8"],
  "brightness": 0.56,
  "saturation": 0.31,
  "orientation": "landscape",
  "story_role": "opening",
  "caption": "THE HARBOR BEFORE RAIN",
  "subjects": ["shoreline", "boat"],
  "dominant_gesture": "horizontal drift",
  "quiet_regions": ["upper sky"]
}
```

## Codex Skill

Copy `skills/moments-to-pages` into your Codex skills directory and restart Codex. Then ask:

```text
Use $moments-to-pages to arrange these travel photos into a quiet visual story.
```

## Privacy and originality

Photos stay local unless the user explicitly chooses another workflow. This repository does not include third-party style references or prompts from similarly themed source-available projects. Its code is licensed under Apache-2.0.

## Roadmap

- printable eight-page foldable zine PDF;
- configurable typography and bilingual captions;
- crop-aware subject placement;
- browser preview and drag-to-reorder editor;
- community-authored visual-system packages.

## License

Apache-2.0. Example photos added by contributors must include their own clear usage terms.
