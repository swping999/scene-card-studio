# Moments to Pages

[中文](README.zh-CN.md) · English

> **This is not a style-transfer repository. It is a Scene Card–based visual narrative engine for personal photography.**

Moments to Pages turns observable photo evidence into editable narrative decisions and deterministic layouts. Instead of asking only *what should these photos look like?*, it asks *how should this story be read?*

```text
photos → observation → visual direction → sequence → narrative system → editable output
```

## Showcase

All source photographs below were generated specifically for this repository. The three boards use the same Scene Cards but express different recording mechanisms.

### Editorial Sequence

![Editorial Sequence example](examples/outputs/editorial-sequence.png)

A spacious photo essay that keeps the photographs primary and makes each frame's story role legible.

### Memory Atlas

![Memory Atlas example](examples/outputs/memory-atlas.png)

A route-led system for departure, distance, return, and spatial memory.

### Field Log

![Field Log example](examples/outputs/field-log.png)

An observational record for documentary detail, notes, and restrained evidence.

[View source photos](examples/photos) · [View generated Scene Cards](examples/generated-story.json) · [Read the originality statement](ORIGINALITY.md)

## The Visual Director layer

Scene Cards explicitly separate visible evidence from interpretation:

```json
{
  "observation": {
    "subjects": ["greenhouse", "work lamp"],
    "dominant_gesture": "repeating window grid",
    "quiet_regions": ["upper evening sky"]
  },
  "direction": {
    "story_role": "opening",
    "narrative_intent": "patient growth",
    "emotional_tone": ["intimate", "hopeful"],
    "director_note": "Treat the lamp as a sign of care, not dramatic spectacle.",
    "confidence": 0.82
  }
}
```

- **Observation** records what is visibly present.
- **Direction** records an editable interpretation.
- **Narrative Systems** decide how the sequence can be read.

The distinction prevents inferred meaning from being presented as photographic fact.

## Narrative Systems, not style filters

The project expands through recording and reading mechanisms such as `family-archive`, `contact-sheet`, `journey-sequence`, `memory-atlas`, `field-log`, and `exhibition-label`. A system must explain what narrative work it performs; a list of aesthetic keywords is not enough.

## Quick start

Requires Python 3.10+. Automatic analysis and PNG rendering use Pillow.

```bash
python -m pip install -e '.[images]'
moments-to-pages analyze photos/*.jpg --output story.json
moments-to-pages recommend story.json
moments-to-pages render story.json --style editorial-sequence --format png --output story.png
moments-to-pages render story.json --style memory-atlas --format svg --output story.svg
```

## Codex Skill

Copy `skills/moments-to-pages` into your Codex skills directory, restart Codex, then ask:

```text
Use $moments-to-pages to direct these photos as a quiet family archive.
```

## Originality and privacy

- no third-party style assets;
- no prompts copied from similarly themed repositories;
- repository examples use newly generated project-owned demo assets;
- the core contribution is the Scene Card + Visual Director + narrative rendering workflow;
- source photos stay local unless the user explicitly chooses otherwise.

See [ORIGINALITY.md](ORIGINALITY.md) for the complete evidence chain.

## Roadmap

- user-editable Visual Director decisions;
- `family-archive`, `contact-sheet`, and `journey-sequence` systems;
- crop-aware subject placement;
- printable PDF and social carousel renderers;
- browser preview and drag-to-reorder editor;
- community-authored Narrative Systems.

## License

Apache-2.0. Example assets must include clear provenance and usage terms.
