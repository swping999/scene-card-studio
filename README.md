# Scene Card Studio

[中文](README.zh-CN.md) · English

> **This is not a style-transfer repository. It is a Scene Card–based visual narrative engine for personal photography.**

Scene Card Studio turns observable photo evidence into editable narrative decisions, versioned generation prompts, directed images, and deterministic layouts. Instead of asking only *what should these photos look like?*, it asks *how should this story be read?*

```text
photos → Scene Cards → Narrative System → Prompt Compiler → image generation → aesthetic review → retry / accept
```

## Before / After

All source photographs below were generated specifically for this repository. Their content is unedited; Before contact sheets use center-cropping only for display. Unless a Narrative System explicitly depends on spatial montage, one source photograph produces one standalone After image.

| Before: original travel photographs | After: AI-composited Memory Atlas |
| --- | --- |
| ![Original photo contact sheet](examples/outputs/before-source-photos.png) | ![Photographic architecture fused with a hand-drawn memory map](examples/outputs/memory-atlas-ai-composite.png) |

[Inspect the three-layer Scene Cards](examples/generated-story.json) · [Prompt Manifest](examples/prompt-manifest.json) · [Render Manifest](examples/render-manifest.json) · [Accepted Review](examples/accepted-review.json)

### Case 2 · Family Archive

| Before: fictional documentary inputs | After: AI-composited family record |
| --- | --- |
| ![Family archive source contact sheet](examples/cases/family-archive/outputs/before.png) | ![Documentary photographs fused with drawings and archive materials](examples/cases/family-archive/outputs/family-archive-ai-composite.png) |

This second case reads repeated gestures—laundry, cooking, sorting photographs—as a record of care passed through generations.

[Inspect the Scene Cards](examples/cases/family-archive/story.json) · [Prompt Manifest](examples/cases/family-archive/prompt-manifest.json) · [Render Manifest](examples/cases/family-archive/render-manifest.json) · [Accepted Review](examples/cases/family-archive/accepted-review.json)

### Case 3 · Cinematic Storyboard

Three unremarkable phone snapshots become three independent film frames. They are connected by a light arc—waiting, pause, departure—not by placing them inside one collage.

| Before: awkward phone snapshot | After: standalone directed frame |
| --- | --- |
| ![Ordinary phone snapshot of a bus stop](examples/cases/cinematic-storyboard/photos/raw-bus-stop.png) | ![Directed rainy-night bus stop frame](examples/cases/cinematic-storyboard/outputs/after-bus-stop.png) |
| ![Ordinary phone snapshot of a diner](examples/cases/cinematic-storyboard/photos/raw-diner.png) | ![Directed diner seen through rain](examples/cases/cinematic-storyboard/outputs/after-diner.png) |
| ![Ordinary phone snapshot of a taxi](examples/cases/cinematic-storyboard/photos/raw-taxi.png) | ![Directed taxi departure frame](examples/cases/cinematic-storyboard/outputs/after-taxi.png) |

[Inspect the Scene Cards](examples/cases/cinematic-storyboard/story.json) · [Open the three compiled prompts](examples/cases/cinematic-storyboard/prompt-manifest.json) · [Inspect a real failed → targeted retry → accepted record](examples/cases/cinematic-storyboard/retry-example/README.md) · [View the source contact sheet](examples/cases/cinematic-storyboard/outputs/before.png)

### Case 4 · Minimal Editorial

This system does not paste three objects onto a designed page. It gives each ordinary object its own photographic stage and lets material, shadow, and negative space do the narrative work.

| Before: cluttered household snapshot | After: standalone art-book photograph |
| --- | --- |
| ![Ordinary phone snapshot of a mug](examples/cases/minimal-editorial/photos/raw-mug.png) | ![Quiet editorial photograph of the same mug](examples/cases/minimal-editorial/outputs/after-mug.png) |
| ![Ordinary phone snapshot of a worn chair](examples/cases/minimal-editorial/photos/raw-chair.png) | ![Sculptural editorial photograph of the same chair](examples/cases/minimal-editorial/outputs/after-chair.png) |
| ![Ordinary phone snapshot of linen](examples/cases/minimal-editorial/photos/raw-linen.png) | ![Material-focused editorial photograph of the same linen](examples/cases/minimal-editorial/outputs/after-linen.png) |

[Inspect the Scene Cards](examples/cases/minimal-editorial/story.json) · [Compiled Prompts](examples/cases/minimal-editorial/prompt-manifest.json) · [Render Manifest](examples/cases/minimal-editorial/render-manifest.json) · [Accepted Review](examples/cases/minimal-editorial/accepted-review.json) · [View the source contact sheet](examples/cases/minimal-editorial/outputs/before.png)

The transformation is not a visual filter. The system separates observation from interpretation, assigns story roles, writes editable director notes, recommends a Narrative System, and can produce either a deterministic workprint or a genuinely transformed presentation image. Spatial and archival systems may use mixed media; cinematic and minimal systems default to one source → one frame.

### Editorial Sequence

![Editorial Sequence example](examples/outputs/editorial-sequence.png)

A spacious photo essay that keeps the photographs primary and makes each frame's story role legible.

### Memory Atlas

![Memory Atlas mixed-media example](examples/outputs/memory-atlas-ai-composite.png)

A mixed-media system for journeys, distance, place, and spatial memory. It keeps actual architecture photographic while allowing the geography between places to become drawn memory; it does not assume that every journey ends in a return.

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

The distinction prevents inferred meaning from being presented as photographic fact. Automatic analysis remains conservative, and every Scene Card decision can be edited before prompt compilation.

## v0.3.3 · Auditable generation contracts

The compiler turns Scene Card evidence, one Narrative System, and one replaceable Expression Profile into a versioned JSON generation contract. Four core systems are supported: `cinematic-storyboard`, `minimal-editorial`, `memory-atlas`, and `family-archive`. The system defines how the story is read; the profile defines how that mechanism is visually expressed. `source-led` is the default.

`memory-atlas` now includes the original `full-watercolor-memory` profile. Unlike `watercolor-contour`, which preserves photographic anchors inside a drawn geography, it repaints people, clothing, architecture, landscape, and transitions in one continuous watercolor medium while preserving identity, pose, spatial evidence, and the source palette. Its contract explicitly rejects photographic pixels, pasted cutout edges, named-artist imitation, and unlicensed style references.

Every compiled prompt contains the same ten modules:

1. subject fidelity;
2. explicit `must_preserve` / `may_transform` / `must_remove` rules;
3. narrative intent;
4. composition;
5. lighting and color;
6. material and surface;
7. spatial relationships;
8. text and label strategy;
9. exclusions;
10. output ratio and format.

Every prompt now carries a structured `output_contract` with exact MIME type, width, height, and aspect ratio. `bind-outputs` decodes the candidate and rejects format or dimension mismatches before review. Optional `reference_output` records are benchmark comparisons only: a formal review must target a Render Manifest containing `candidate_output` records.

Sequence systems additionally review subject continuity, light/color continuity, rhythm, and narrative arc. Retry provenance is a closed hash chain: Prompt Manifest → failed Render Manifest → failed Review → Retry Manifest → post-retry Render Manifest → accepted Review. Each link records its parent hash and chronology.

## Narrative Systems, not style filters

The project expands through recording and reading mechanisms such as `family-archive`, `cinematic-storyboard`, `minimal-editorial`, `contact-sheet`, `journey-sequence`, `memory-atlas`, `field-log`, and `exhibition-label`. A system must explain what narrative work it performs; a list of aesthetic keywords is not enough.

## Quick start

Requires Python 3.10+. Automatic analysis and PNG rendering use Pillow.

```bash
python -m pip install -e '.[images]'
scene-card-studio analyze photos/*.jpg --output story.json
scene-card-studio recommend story.json
scene-card-studio compile story.json --system cinematic-storyboard --expression-profile source-led --output prompt-manifest.json
scene-card-studio compile story.json --system memory-atlas --expression-profile full-watercolor-memory --output watercolor-memory-manifest.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio render story.json --style memory-atlas --format svg --output story.svg
scene-card-studio render story.json --style field-log --mode workprint --format png --output notes.png
scene-card-studio bind-outputs prompt-manifest.json --result cinematic-storyboard-01=after-01.png --output render-manifest.json
scene-card-studio retry render-manifest.json assessment.json --output retry-manifest.json
scene-card-studio bind-outputs retry-manifest.json --result cinematic-storyboard-01=after-01-retry.png --output post-retry-render-manifest.json
scene-card-studio consent prompt-manifest.json --provider PROVIDER --purpose "presentation synthesis" --confirm --output upload-consent.json
```

`compile` emits one prompt per source for cinematic and minimal systems, and one multi-source prompt for spatial and archival systems. Cloud synthesis requires an explicit consent record containing the provider, purpose, and exact upload list; without it, the Skill stops at local Workprint and Prompt Manifest. Formal review refuses an unbound Prompt Manifest. Safe SVG embedding fully decodes and re-encodes raster images, strips appended data and metadata, and enforces source-byte and pixel limits. `presentation` is the default layout mode; use `--mode workprint` when you want observations, interpretations, roles, and direction notes visible.

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

See [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) for the versioned provenance record and [example asset terms](examples/ASSET_LICENSE.md) for per-asset licensing.

## Roadmap

- user-editable Visual Director decisions;
- `contact-sheet` and `journey-sequence` systems;
- crop-aware subject placement;
- image-model adapters and queued generation;
- printable PDF and social carousel renderers;
- browser preview and drag-to-reorder editor;
- community-authored Narrative Systems.

## License

Code and repository-specific demo assets are Apache-2.0; the bundled font remains under SIL OFL 1.1. See [example asset terms](examples/ASSET_LICENSE.md).
