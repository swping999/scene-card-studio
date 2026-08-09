# Scene Card Studio

[中文](README.zh-CN.md) · English

> **This is not a style-transfer repository. It is a Scene Card–based visual narrative engine for personal photography.**

Scene Card Studio turns observable photo evidence into editable narrative decisions and deterministic layouts. Instead of asking only *what should these photos look like?*, it asks *how should this story be read?*

```text
photos → observation → interpretation → visual direction → sequence → narrative system → editable output
```

## Before / After

All source photographs below were generated specifically for this repository. Every comparison keeps the untouched input visible. Unless a Narrative System explicitly depends on spatial montage, one source photograph produces one standalone After image.

| Before: original travel photographs | After: AI-composited Memory Atlas |
| --- | --- |
| ![Original photo contact sheet](examples/outputs/before-source-photos.png) | ![Photographic architecture fused with a hand-drawn memory map](examples/outputs/memory-atlas-ai-composite.png) |

[Inspect the three-layer Scene Cards for this case](examples/generated-story.json)

### Case 2 · Family Archive

| Before: fictional documentary inputs | After: AI-composited family record |
| --- | --- |
| ![Family archive source contact sheet](examples/cases/family-archive/outputs/before.png) | ![Documentary photographs fused with drawings and archive materials](examples/cases/family-archive/outputs/family-archive-ai-composite.png) |

This second case reads repeated gestures—laundry, cooking, sorting photographs—as a record of care passed through generations.

[Inspect the Family Archive Scene Cards](examples/cases/family-archive/story.json)

### Case 3 · Cinematic Storyboard

Three unremarkable phone snapshots become three independent film frames. They are connected by a light arc—waiting, pause, departure—not by placing them inside one collage.

| Before: awkward phone snapshot | After: standalone directed frame |
| --- | --- |
| ![Ordinary phone snapshot of a bus stop](examples/cases/cinematic-storyboard/photos/raw-bus-stop.png) | ![Directed rainy-night bus stop frame](examples/cases/cinematic-storyboard/outputs/after-bus-stop.png) |
| ![Ordinary phone snapshot of a diner](examples/cases/cinematic-storyboard/photos/raw-diner.png) | ![Directed diner seen through rain](examples/cases/cinematic-storyboard/outputs/after-diner.png) |
| ![Ordinary phone snapshot of a taxi](examples/cases/cinematic-storyboard/photos/raw-taxi.png) | ![Directed taxi departure frame](examples/cases/cinematic-storyboard/outputs/after-taxi.png) |

[Inspect the three-layer Scene Cards](examples/cases/cinematic-storyboard/story.json) · [View the untouched source contact sheet](examples/cases/cinematic-storyboard/outputs/before.png)

### Case 4 · Minimal Editorial

This system does not paste three objects onto a designed page. It gives each ordinary object its own photographic stage and lets material, shadow, and negative space do the narrative work.

| Before: cluttered household snapshot | After: standalone art-book photograph |
| --- | --- |
| ![Ordinary phone snapshot of a mug](examples/cases/minimal-editorial/photos/raw-mug.png) | ![Quiet editorial photograph of the same mug](examples/cases/minimal-editorial/outputs/after-mug.png) |
| ![Ordinary phone snapshot of a worn chair](examples/cases/minimal-editorial/photos/raw-chair.png) | ![Sculptural editorial photograph of the same chair](examples/cases/minimal-editorial/outputs/after-chair.png) |
| ![Ordinary phone snapshot of linen](examples/cases/minimal-editorial/photos/raw-linen.png) | ![Material-focused editorial photograph of the same linen](examples/cases/minimal-editorial/outputs/after-linen.png) |

[Inspect the three-layer Scene Cards](examples/cases/minimal-editorial/story.json) · [View the untouched source contact sheet](examples/cases/minimal-editorial/outputs/before.png)

The transformation is not a visual filter. The system separates observation from interpretation, assigns story roles, writes editable director notes, recommends a Narrative System, and can produce either a deterministic workprint or a genuinely transformed presentation image. Spatial and archival systems may use mixed media; cinematic and minimal systems default to one source → one frame.

### Editorial Sequence

![Editorial Sequence example](examples/outputs/editorial-sequence.png)

A spacious photo essay that keeps the photographs primary and makes each frame's story role legible.

### Memory Atlas

![Memory Atlas mixed-media example](examples/outputs/memory-atlas-ai-composite.png)

A mixed-media system for departure, distance, return, and spatial memory. It keeps actual architecture photographic while allowing the geography between places to become drawn memory.

### Field Log

![Field Log example](examples/outputs/field-log.png)

An observational record for documentary detail, notes, and restrained evidence.

[View source photos](examples/photos) · [View generated Scene Cards](examples/generated-story.json) · [Read the design principles](DESIGN_PRINCIPLES.md)

## The Visual Director layer

Scene Cards explicitly separate visible evidence from interpretation:

```json
{
  "observation": {
    "subjects": ["greenhouse", "work lamp"],
    "dominant_gesture": "repeating window grid",
    "quiet_regions": ["upper evening sky"]
  },
  "interpretation": {
    "narrative_intent": "patient growth",
    "emotional_tone": ["intimate", "hopeful"],
    "confidence": 0.82,
    "method": "manually-directed example"
  },
  "direction": {
    "story_role": "opening",
    "director_note": "Treat the lamp as a sign of care, not dramatic spectacle."
  }
}
```

- **Observation** records what is visibly present.
- **Interpretation** records a tentative theme and emotional reading.
- **Direction** records editable sequencing and layout decisions.
- **Narrative Systems** decide how the sequence can be read.

The distinction prevents inferred meaning from being presented as photographic fact. Advanced narrative fields in the showcase are explicitly marked as manually directed; the current analyzer provides only low-confidence heuristics.

## Narrative Systems, not style filters

The project expands through recording and reading mechanisms such as `family-archive`, `cinematic-storyboard`, `minimal-editorial`, `contact-sheet`, `journey-sequence`, `memory-atlas`, `field-log`, and `exhibition-label`. A system must explain what narrative work it performs; a list of aesthetic keywords is not enough.

## Quick start

Requires Python 3.10+. Automatic analysis and PNG rendering use Pillow.

```bash
python -m pip install -e '.[images]'
scene-card-studio analyze photos/*.jpg --output story.json
scene-card-studio recommend story.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio render story.json --style memory-atlas --format svg --output story.svg
scene-card-studio render story.json --style field-log --mode workprint --format png --output notes.png
```

`presentation` is the default and hides internal director terminology. Use `--mode workprint` when you want observations, interpretations, roles, and direction notes visible. Output height grows with the number of photographs, and source paths are resolved relative to the Scene Card JSON file.

## Codex Skill

Copy `skills/scene-card-studio` into your Codex skills directory, restart Codex, then ask:

```text
Use $scene-card-studio to direct these photos as a quiet family archive.
```

## Originality and privacy

- no third-party style assets;
- no prompts copied from similarly themed repositories;
- repository examples use newly generated project-owned demo assets;
- the core contribution is the Scene Card + Visual Director + narrative rendering workflow;
- source photos stay local unless the user explicitly chooses otherwise.

See [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) for the complete evidence chain.

## Roadmap

- user-editable Visual Director decisions;
- `contact-sheet` and `journey-sequence` systems;
- crop-aware subject placement;
- printable PDF and social carousel renderers;
- browser preview and drag-to-reorder editor;
- community-authored Narrative Systems.

## License

Apache-2.0. Example assets must include clear provenance and usage terms.
