# Scene Card Studio

[中文](README.zh-CN.md) · English

> **This is not a style-transfer repository. It is a Scene Card–based visual narrative engine for personal photography.**

Scene Card Studio turns observable photo evidence into editable narrative decisions and deterministic layouts. Instead of asking only *what should these photos look like?*, it asks *how should this story be read?*

```text
photos → observation → interpretation → visual direction → sequence → narrative system → editable output
```

## Before / After

All source photographs below were generated specifically for this repository. The Before board shows the untouched inputs; each After board uses the same Scene Cards with a different recording mechanism.

| Before: original photo set | After: directed narrative |
| --- | --- |
| ![Original photo contact sheet](examples/outputs/before-source-photos.png) | ![Editorial Sequence result](examples/outputs/editorial-sequence.png) |

### Case 2 · Family Archive

| Before: fictional documentary inputs | After: family record |
| --- | --- |
| ![Family archive source contact sheet](examples/cases/family-archive/outputs/before.png) | ![Family Archive narrative result](examples/cases/family-archive/outputs/after.png) |

This second case reads repeated gestures—laundry, cooking, sorting photographs—as a record of care passed through generations.

The transformation is not a visual filter. The system separates observation from interpretation, assigns story roles, writes editable director notes, recommends a Narrative System, and then renders the sequence.

### Editorial Sequence

![Editorial Sequence example](examples/outputs/editorial-sequence.png)

A spacious photo essay that keeps the photographs primary and makes each frame's story role legible.

### Memory Atlas

![Memory Atlas example](examples/outputs/memory-atlas.png)

A route-led system for departure, distance, return, and spatial memory.

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

The project expands through recording and reading mechanisms such as `family-archive`, `contact-sheet`, `journey-sequence`, `memory-atlas`, `field-log`, and `exhibition-label`. A system must explain what narrative work it performs; a list of aesthetic keywords is not enough.

## Quick start

Requires Python 3.10+. Automatic analysis and PNG rendering use Pillow.

```bash
python -m pip install -e '.[images]'
scene-card-studio analyze photos/*.jpg --output story.json
scene-card-studio recommend story.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio render story.json --style memory-atlas --format svg --output story.svg
```

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
