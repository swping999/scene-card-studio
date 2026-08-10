# Scene Card Studio

[中文](README.zh-CN.md) · English

[![Scene Card Studio opening film](docs/media/scene-card-studio-opening.gif)](docs/media/scene-card-studio-opening.mp4)

▶ [Play the 3-second opening film](docs/media/scene-card-studio-opening.mp4)

> **This is not a style-transfer repository. It is a Scene Card–based visual narrative engine for personal photography.**

Scene Card Studio turns observable photo evidence into editable narrative decisions, versioned generation prompts, directed images, and deterministic layouts. Instead of asking only *what should these photos look like?*, it asks *how should this story be read?*

```text
photos → Scene Cards → Narrative System → Prompt Compiler → image generation → aesthetic review → retry / accept
```

## Before / After

Every Before below is a newly generated, deliberately unpolished phone-style source made for this repository. Every After is a materially redirected image of that source—not the same image inside a border, contact sheet, or decorative collage. The people are fictional AI-generated subjects.

### 1 · Cinematic Sequence

| Before · flat metro snapshot | After · motivated rain, light, and frame geometry |
| --- | --- |
| ![Unpolished metro snapshot](examples/cases/v0.4-gallery/before/cinematic-sequence.jpg) | ![Directed cinematic night frame](examples/cases/v0.4-gallery/after/cinematic-sequence.jpg) |

### 2 · Memory Atlas

| Before · roadside building | After · real architecture fused with drawn geography |
| --- | --- |
| ![Ordinary roadside building](examples/cases/v0.4-gallery/before/memory-atlas.jpg) | ![Photographic building integrated with watercolor terrain](examples/cases/v0.4-gallery/after/memory-atlas.jpg) |

### 3 · Family Chronicle

| Before · cluttered domestic snapshot | After · one intimate photographic-drawing record |
| --- | --- |
| ![Ordinary laundry-folding snapshot](examples/cases/v0.4-gallery/before/family-chronicle.jpg) | ![Directed family chronicle](examples/cases/v0.4-gallery/after/family-chronicle.jpg) |

### 4 · Quiet Editorial

| Before · cluttered kettle photo | After · quiet material study |
| --- | --- |
| ![Ordinary kettle snapshot](examples/cases/v0.4-gallery/before/quiet-editorial.jpg) | ![Quiet editorial kettle photograph](examples/cases/v0.4-gallery/after/quiet-editorial.jpg) |

### 5 · Editorial Rhythm

| Before · accidental chair arrangement | After · color, spacing, crop, and shadow as rhythm |
| --- | --- |
| ![Ordinary plastic chairs](examples/cases/v0.4-gallery/before/editorial-rhythm.jpg) | ![Directed chair rhythm](examples/cases/v0.4-gallery/after/editorial-rhythm.jpg) |

### 6 · Field Log

| Before · casual repair snapshot | After · factual observational record |
| --- | --- |
| ![Ordinary bicycle repair snapshot](examples/cases/v0.4-gallery/before/field-log.jpg) | ![Directed field-log photograph](examples/cases/v0.4-gallery/after/field-log.jpg) |

### 7 · Watercolor Chronicle

| Before · ordinary seaside portrait | After · person, clothing, objects, and place repainted together |
| --- | --- |
| ![Ordinary seaside portrait](examples/cases/v0.4-gallery/before/watercolor-chronicle.jpg) | ![Fully repainted watercolor chronicle](examples/cases/v0.4-gallery/after/watercolor-chronicle.jpg) |

### 8 · Heritage Portrait

| Before · flash-lit living room | After · restrained silver-gelatin and hand-colored portrait |
| --- | --- |
| ![Ordinary portrait snapshot](examples/cases/v0.4-gallery/before/heritage-portrait.jpg) | ![Directed heritage portrait](examples/cases/v0.4-gallery/after/heritage-portrait.jpg) |

### 9 · Museum Catalogue

| Before · object in storage clutter | After · inspectable conservation plate |
| --- | --- |
| ![Radio in a cluttered storage space](examples/cases/v0.4-gallery/before/museum-catalogue.jpg) | ![Museum catalogue radio plate](examples/cases/v0.4-gallery/after/museum-catalogue.jpg) |

### 10 · Travel Journal

| Before · waiting-platform snapshot | After · railway space becomes a tactile route field |
| --- | --- |
| ![Ordinary suitcase at a station](examples/cases/v0.4-gallery/before/travel-journal.jpg) | ![Seamless travel journal image](examples/cases/v0.4-gallery/after/travel-journal.jpg) |

### 11 · Street Reportage

| Before · loose rainy crosswalk frame | After · decisive monochrome public-life frame |
| --- | --- |
| ![Ordinary rainy crosswalk snapshot](examples/cases/v0.4-gallery/before/street-reportage.jpg) | ![Directed black-and-white street reportage](examples/cases/v0.4-gallery/after/street-reportage.jpg) |

### 12 · Fashion Editorial

| Before · bland mall portrait | After · garment-led architectural frame |
| --- | --- |
| ![Ordinary mall portrait](examples/cases/v0.4-gallery/before/fashion-editorial.jpg) | ![Directed fashion editorial](examples/cases/v0.4-gallery/after/fashion-editorial.jpg) |

### 13 · Dream Logic

| Before · child with one kite | After · one coherent impossible rule, identity locked |
| --- | --- |
| ![Ordinary salt-flat kite snapshot](examples/cases/v0.4-gallery/before/dream-logic.jpg) | ![Single-kite dream-logic transformation](examples/cases/v0.4-gallery/after/dream-logic.jpg) |

The first ten entries are Narrative Systems. Watercolor Chronicle, Heritage Portrait, and Dream Logic are replaceable Expression Profiles applied through compatible systems. This keeps story structure separate from surface language.

[Inspect all 13 Scene Cards and direction records](examples/cases/v0.4-gallery/case-records.json) · [Read the case notes](examples/cases/v0.4-gallery/README.md) · [Read the design principles](DESIGN_PRINCIPLES.md)

## Earlier benchmark cases

The original benchmark cases remain part of the repository and retain their manifests, bound outputs, reviews, and retry records.

### Original Memory Atlas benchmark

| Before: original travel photographs | After: AI-composited Memory Atlas |
| --- | --- |
| ![Original photo contact sheet](examples/outputs/before-source-photos.png) | ![Photographic architecture fused with a hand-drawn memory map](examples/outputs/memory-atlas-ai-composite.png) |

[Scene Cards](examples/generated-story.json) · [Prompt Manifest](examples/prompt-manifest.json) · [Render Manifest](examples/render-manifest.json) · [Accepted Review](examples/accepted-review.json)

### Original Family Archive benchmark

| Before: fictional documentary inputs | After: AI-composited family record |
| --- | --- |
| ![Family archive source contact sheet](examples/cases/family-archive/outputs/before.png) | ![Documentary photographs fused with drawings and archive materials](examples/cases/family-archive/outputs/family-archive-ai-composite.png) |

[Scene Cards](examples/cases/family-archive/story.json) · [Prompt Manifest](examples/cases/family-archive/prompt-manifest.json) · [Render Manifest](examples/cases/family-archive/render-manifest.json) · [Accepted Review](examples/cases/family-archive/accepted-review.json)

### Original Cinematic Storyboard benchmark

| Before: awkward phone snapshot | After: standalone directed frame |
| --- | --- |
| ![Ordinary phone snapshot of a bus stop](examples/cases/cinematic-storyboard/photos/raw-bus-stop.png) | ![Directed rainy-night bus stop frame](examples/cases/cinematic-storyboard/outputs/after-bus-stop.png) |
| ![Ordinary phone snapshot of a diner](examples/cases/cinematic-storyboard/photos/raw-diner.png) | ![Directed diner seen through rain](examples/cases/cinematic-storyboard/outputs/after-diner.png) |
| ![Ordinary phone snapshot of a taxi](examples/cases/cinematic-storyboard/photos/raw-taxi.png) | ![Directed taxi departure frame](examples/cases/cinematic-storyboard/outputs/after-taxi.png) |

[Scene Cards](examples/cases/cinematic-storyboard/story.json) · [Compiled prompts](examples/cases/cinematic-storyboard/prompt-manifest.json) · [Failed → targeted retry → accepted record](examples/cases/cinematic-storyboard/retry-example/README.md) · [Source contact sheet](examples/cases/cinematic-storyboard/outputs/before.png)

### Original Minimal Editorial benchmark

| Before: cluttered household snapshot | After: standalone art-book photograph |
| --- | --- |
| ![Ordinary phone snapshot of a mug](examples/cases/minimal-editorial/photos/raw-mug.png) | ![Quiet editorial photograph of the same mug](examples/cases/minimal-editorial/outputs/after-mug.png) |
| ![Ordinary phone snapshot of a worn chair](examples/cases/minimal-editorial/photos/raw-chair.png) | ![Sculptural editorial photograph of the same chair](examples/cases/minimal-editorial/outputs/after-chair.png) |
| ![Ordinary phone snapshot of linen](examples/cases/minimal-editorial/photos/raw-linen.png) | ![Material-focused editorial photograph of the same linen](examples/cases/minimal-editorial/outputs/after-linen.png) |

[Scene Cards](examples/cases/minimal-editorial/story.json) · [Compiled prompts](examples/cases/minimal-editorial/prompt-manifest.json) · [Render Manifest](examples/cases/minimal-editorial/render-manifest.json) · [Accepted Review](examples/cases/minimal-editorial/accepted-review.json) · [Source contact sheet](examples/cases/minimal-editorial/outputs/before.png)

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

## v0.4.0 · Systems, Profiles, and deterministic typography

The compiler turns Scene Card evidence, one Narrative System, and one replaceable Expression Profile into a versioned JSON generation contract. Ten Narrative Systems are supported. The system defines how the story is read; the Profile defines how that mechanism is visually expressed. `source-led` remains the default.

| Narrative System | Display name | Reading mechanism |
| --- | --- | --- |
| `cinematic-storyboard` | Cinematic Sequence | temporal continuity, motivated light, shot relationships |
| `memory-atlas` | Memory Atlas | place, distance, direction, spatial memory |
| `family-archive` | Family Chronicle | repeated supplied people, objects, gestures, and time |
| `minimal-editorial` | Quiet Editorial | hierarchy, negative space, light, material rhythm |
| `editorial-sequence` | Editorial Rhythm | sequence, scale, contrast, density, pause |
| `field-log` | Field Log | observed evidence and documentary context |
| `museum-catalogue` | Museum Catalogue | inspectable plates and supplied collection metadata |
| `travel-journal` | Travel Journal | movement, pauses, thresholds, supplied journey evidence |
| `street-reportage` | Street Reportage | observed public gestures and factual sequence |
| `fashion-editorial` | Fashion Editorial | pose, garment construction, crop, shot-scale rhythm |

Reusable Profiles include `watercolor-chronicle`, `heritage-portrait`, and the stricter identity-locked `dream-logic`. The v0.3.3 name `full-watercolor-memory` remains a compatibility alias for `watercolor-chronicle` inside Memory Atlas.

Visible text is no longer delegated to the image model. Every Manifest includes a `presentation_contract`; `scene-card-studio present` applies only supplied captions, dates, locations, collection names, and catalogue identifiers as a deterministic SVG overlay. Missing metadata is omitted rather than inferred.

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

The project expands through recording and reading mechanisms, not a flat menu of visual effects. Watercolor, heritage photographic process, monochrome treatment, and dream logic remain replaceable Profiles. A system must explain what narrative work it performs; a list of aesthetic keywords is not enough.

## Quick start

Requires Python 3.10+. Automatic analysis and PNG rendering use Pillow.

```bash
python -m pip install -e '.[images]'
scene-card-studio analyze photos/*.jpg --output story.json
scene-card-studio recommend story.json
scene-card-studio compile story.json --system cinematic-storyboard --expression-profile source-led --output prompt-manifest.json
scene-card-studio compile story.json --system memory-atlas --expression-profile watercolor-chronicle --output watercolor-memory-manifest.json
scene-card-studio compile story.json --system museum-catalogue --expression-profile heritage-portrait --output catalogue-manifest.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio render story.json --style memory-atlas --format svg --output story.svg
scene-card-studio render story.json --style field-log --mode workprint --format png --output notes.png
scene-card-studio bind-outputs prompt-manifest.json --result cinematic-storyboard-01=after-01.png --output render-manifest.json
scene-card-studio present render-manifest.json --output presentation.svg
scene-card-studio retry render-manifest.json assessment.json --output retry-manifest.json
scene-card-studio bind-outputs retry-manifest.json --result cinematic-storyboard-01=after-01-retry.png --output post-retry-render-manifest.json
scene-card-studio consent prompt-manifest.json --provider PROVIDER --purpose "presentation synthesis" --confirm --output upload-consent.json
```

`compile` emits one prompt per source for Cinematic, Quiet Editorial, Editorial Rhythm, Field Log, Museum, Street, and Fashion systems; Memory Atlas, Family Chronicle, and Travel Journal use multi-source synthesis. Cloud synthesis requires explicit consent containing the provider, purpose, and exact upload list. Formal review refuses an unbound Prompt Manifest. `present` verifies bound output hashes and keeps generated pixels separate from deterministic text. Safe SVG embedding fully decodes and re-encodes raster images, strips appended data and metadata, and enforces source-byte and pixel limits.

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
