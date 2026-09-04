<h1 align="center">Scene Card Studio</h1>

<p align="center"><strong>AI visual director for turning personal photos into structured, editable visual narratives.</strong></p>

<p align="center">
  <a href="https://github.com/swping999/scene-card-studio/releases/tag/v0.7.0"><img alt="Version 0.7.0" src="https://img.shields.io/badge/version-0.7.0-315c8c?style=flat-square"></a>
  <a href="https://github.com/swping999/scene-card-studio/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/swping999/scene-card-studio/ci.yml?branch=main&style=flat-square&label=tests"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-315c8c?style=flat-square">
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827?style=flat-square">
  <a href="LICENSE"><img alt="Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-315c8c?style=flat-square"></a>
</p>

<p align="center"><a href="README.zh-CN.md">中文</a> · English</p>

[![Scene Card Studio opening film](docs/media/scene-card-studio-opening.gif)](docs/media/scene-card-studio-opening.mp4)

▶ [Play the 6-second opening film](docs/media/scene-card-studio-opening.mp4)

> **This is not a style-transfer repository. It is a Scene Card–based visual narrative engine for personal photography.**

Scene Card Studio turns observable photo evidence into editable narrative decisions, versioned generation prompts, directed images, and deterministic layouts. Instead of asking only *what should these photos look like?*, it asks *how should this story be read?*

```text
photos → Scene Cards → Narrative System → Prompt Compiler → image generation → aesthetic review → retry / accept
```

### One command to start

After installation, one local command turns one photo or a related set into draft Scene Cards, an automatically routed Prompt Manifest, a clearly labelled analysis Workprint, and a run summary:

```bash
scene-card-studio direct photos/portrait.jpg \
  --brief "a restrained hand-colored heritage portrait"
```

Use multiple paths or a glob for a sequence. `direct` selects a Narrative System from the bilingual brief and selects a non-default Expression Profile only when the brief explicitly asks for it. Its local analyzer measures dimensions, orientation, palette, brightness, and saturation; it does **not** pretend that those statistics identify people, objects, gestures, or spatial meaning. Until those semantic fields and transformation rules are completed, the bundle is labelled `needs-semantic-direction` and upload consent is refused. This preparation step never uploads a source photo and never presents its Workprint as a generated After.

| At a glance | Project contract |
| --- | --- |
| Input | One photograph or a related photo sequence |
| Direction | Observable evidence → editable interpretation → explicit art direction |
| Visual vocabulary | 11 Narrative Systems + 22 replaceable Expression Profiles |
| Output | Local workprints, versioned prompts, contract-checked images, deterministic typography, review records |
| Privacy | Local-first analysis; cloud upload requires provider-, purpose-, and file-specific consent |

**Explore:** [Before / After](#before--after) · [Visual Director](#the-visual-director-layer) · [Systems and Profiles](#current-systems-profiles-and-deterministic-typography) · [Quick start](#quick-start) · [Contributing](CONTRIBUTING.md)

### One photo or many

- **One photo → one directed After.** Choose a compatible Narrative System and Expression Profile, then produce one standalone After. A single photo is never forced into a contact sheet, sequence, or decorative collage.
- **Many photos → one coherent story.** Use per-photo direction when every source needs its own After, or choose a synthesis system when place, journey, or repeated relationships need to share one artifact.
- **Style remains editable.** The Narrative System controls how the image or story is read; the Expression Profile controls how it is visually expressed. A single photo can therefore use `source-led`, `watercolor-chronicle`, `heritage-portrait`, `dream-logic`, or another profile supported by the selected system.

Check compatible combinations with `scene-card-studio profiles`. The compiler records `single-photo`, `multi-photo-per-source`, or `multi-photo-synthesis` in every Manifest so downstream tools cannot silently change the requested source mode.

## After-only Director Gallery · v0.7

The public showcase leads with the finished After image. These three new cases are designed to make the visual difference obvious: a real subject with a relief environment, a restrained ink-and-paper editorial, and a sparse travel-zine page. Older Before/After evidence cases remain below and are not deleted.

| Selective Material Relief | Chinese Photo Editorial | Travel Zine |
| --- | --- | --- |
| [![Real boat with relief mountains](examples/cases/v0.7-director-gallery/after/selective-material-relief.png)](examples/cases/v0.7-director-gallery/after/selective-material-relief.png) | [![Ink-and-paper coastal photo editorial](examples/cases/v0.7-director-gallery/after/chinese-photo-editorial.png)](examples/cases/v0.7-director-gallery/after/chinese-photo-editorial.png) | [![Sparse travel zine railway image](examples/cases/v0.7-director-gallery/after/travel-zine.png)](examples/cases/v0.7-director-gallery/after/travel-zine.png) |

[Open the v0.7 After-only gallery and asset records](examples/cases/v0.7-director-gallery/README.md)

### Selected After Gallery · strongest material cases

These are the most visually distinctive finished images in the repository. The complete evidence galleries remain below; this top section is intentionally curated for first-time visitors.

| Relief environment | Ink editorial | Travel zine |
| --- | --- | --- |
| [![Real boat with relief mountains](examples/cases/v0.7-director-gallery/after/selective-material-relief.png)](examples/cases/v0.7-director-gallery/after/selective-material-relief.png) | [![Ink-and-paper coastal photo editorial](examples/cases/v0.7-director-gallery/after/chinese-photo-editorial.png)](examples/cases/v0.7-director-gallery/after/chinese-photo-editorial.png) | [![Sparse travel zine railway image](examples/cases/v0.7-director-gallery/after/travel-zine.png)](examples/cases/v0.7-director-gallery/after/travel-zine.png) |
| [![Continuous threaded lake landscape](examples/cases/v0.6-gallery/after/threaded-landscape.png)](examples/cases/v0.6-gallery/after/threaded-landscape.png) | [![Layered paper relief landscape](examples/cases/v0.6-gallery/after/paper-relief-landscape.png)](examples/cases/v0.6-gallery/after/paper-relief-landscape.png) | [![Opaque gouache place study](examples/cases/v0.6-gallery/after/gouache-place-study.png)](examples/cases/v0.6-gallery/after/gouache-place-study.png) |
| [![Mineral ink bridge memory](examples/cases/v0.6-gallery/after/mineral-ink-memory.png)](examples/cases/v0.6-gallery/after/mineral-ink-memory.png) | [![Impasto lake light study](examples/cases/v0.6-gallery/after/impasto-light-study.png)](examples/cases/v0.6-gallery/after/impasto-light-study.png) | [![Cyanotype field-object archive](examples/cases/v0.6-gallery/after/cyanotype-archive.png)](examples/cases/v0.6-gallery/after/cyanotype-archive.png) |

## Before / After

### Landscape-led expansion

These new cases deliberately favor places and objects over portraits. Each Before is a newly generated, ordinary source image; each After materially rebuilds the same evidence through a distinct narrative or material system. The opening Journey Taxonomy case classifies a place by movement, landmark, water, vegetation, weather, and material—without copying the supplied social reference's palette, repeated photograph, sticker column, connector lines, or caption layout.

#### Featured Material Narratives

Four of the strongest landscape cases form a focused material family: opaque gouache, a physically sculpted miniature, continuous textile relief, and layered paper relief. Select an image to open its full Before/After case below.

| Gouache Place Study | Sculpted Place Diorama · 3D |
| --- | --- |
| [![Gouache observatory place study](examples/cases/v0.6-gallery/after/gouache-place-study.png)](#gouache-place-study) | [![Sculpted three-dimensional salt-marsh diorama](examples/cases/v0.6-gallery/after/sculpted-place-diorama.png)](#sculpted-place-diorama--3d) |
| **Threaded Landscape · textile relief** | **Paper Relief Landscape** |
| [![Threaded textile relief of the lake and boat](examples/cases/v0.6-gallery/after/threaded-landscape.png)](#threaded-landscape--textile-relief) | [![Cut-paper relief landscape](examples/cases/v0.6-gallery/after/paper-relief-landscape.png)](#paper-relief-landscape) |

#### Journey Taxonomy

| Before · ordinary salt-marsh view | After · one semantic place field, not a sticker board |
| --- | --- |
| ![Ordinary salt-marsh boardwalk](examples/cases/v0.6-gallery/before/salt-marsh-boardwalk.png) | ![Journey Taxonomy landscape](examples/cases/v0.6-gallery/after/journey-taxonomy.png) |

#### Mineral Ink Memory

| Before · cluttered winter bridge | After · continuous mineral pigment and ink |
| --- | --- |
| ![Ordinary winter stone bridge](examples/cases/v0.6-gallery/before/stone-bridge.png) | ![Mineral ink bridge memory](examples/cases/v0.6-gallery/after/mineral-ink-memory.png) |

#### Impasto Light Study

| Before · flat overcast lake | After · light organized through physical paint depth |
| --- | --- |
| ![Ordinary mountain-lake snapshot](examples/cases/v0.6-gallery/before/mountain-lake.png) | ![Impasto mountain-lake light study](examples/cases/v0.6-gallery/after/impasto-light-study.png) |

#### Pixel Diary

| Before · empty market lane | After · one authored pixel grid and depth system |
| --- | --- |
| ![Ordinary empty market lane](examples/cases/v0.6-gallery/before/empty-market-lane.png) | ![Pixel diary market lane](examples/cases/v0.6-gallery/after/pixel-diary.png) |

#### Risograph Route

| Before · literal route through a marsh | After · limited-ink route rhythm |
| --- | --- |
| ![Ordinary salt-marsh route](examples/cases/v0.6-gallery/before/salt-marsh-boardwalk.png) | ![Risograph route print](examples/cases/v0.6-gallery/after/risograph-route.png) |

#### Gouache Place Study

| Before · harsh highland snapshot | After · opaque matte place painting |
| --- | --- |
| ![Ordinary highland observatory](examples/cases/v0.6-gallery/before/highland-observatory.png) | ![Gouache observatory place study](examples/cases/v0.6-gallery/after/gouache-place-study.png) |

#### Cyanotype Archive

| Before · messy field desk | After · evidence-bound contact-print study |
| --- | --- |
| ![Ordinary field objects on a desk](examples/cases/v0.6-gallery/before/field-desk.png) | ![Cyanotype field-object archive](examples/cases/v0.6-gallery/after/cyanotype-archive.png) |

#### Paper Relief Landscape

| Before · flat winter terrain | After · one physically coherent paper relief |
| --- | --- |
| ![Ordinary stone bridge and terraces](examples/cases/v0.6-gallery/before/stone-bridge.png) | ![Cut-paper relief landscape](examples/cases/v0.6-gallery/after/paper-relief-landscape.png) |

#### Autochrome Memory

| Before · casual lake stop | After · restrained early-color material memory |
| --- | --- |
| ![Ordinary mountain lake and boat](examples/cases/v0.6-gallery/before/mountain-lake.png) | ![Autochrome-inspired lake memory](examples/cases/v0.6-gallery/after/autochrome-memory.png) |

#### Pixel + Ink Memory · experimental

| Before · one photographic surface | After · near evidence in pixels, distance in ink |
| --- | --- |
| ![Ordinary empty market lane](examples/cases/v0.6-gallery/before/empty-market-lane.png) | ![Pixel and ink market memory](examples/cases/v0.6-gallery/after/pixel-ink-memory.png) |

#### Sculpted Place Diorama · 3D

| Before · flat landscape photograph | After · physical miniature topology and real volume |
| --- | --- |
| ![Ordinary salt-marsh boardwalk](examples/cases/v0.6-gallery/before/salt-marsh-boardwalk.png) | ![Sculpted three-dimensional salt-marsh diorama](examples/cases/v0.6-gallery/after/sculpted-place-diorama.png) |

#### Threaded Landscape · textile relief

| Before · flat lake snapshot | After · one continuous woven and embroidered relief |
| --- | --- |
| ![Ordinary mountain lake and boat](examples/cases/v0.6-gallery/before/mountain-lake.png) | ![Threaded textile relief of the lake and boat](examples/cases/v0.6-gallery/after/threaded-landscape.png) |

[Inspect the 12 Scene Cards](examples/cases/v0.6-gallery/case-records.json) · [Open the recompilable evidence index](examples/cases/v0.6-gallery/evidence/index.json) · [Read the originality and case notes](examples/cases/v0.6-gallery/README.md)

## Previous v0.4 Before / After

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

| Before · ordinary reading-corner snapshot | After · gentle silver-gelatin and hand-colored portrait |
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

[Inspect all 13 Scene Cards and direction records](examples/cases/v0.4-gallery/case-records.json) · [Open the recompilable evidence index](examples/cases/v0.4-gallery/evidence/index.json) · [Read the case notes](examples/cases/v0.4-gallery/README.md) · [Read the design principles](DESIGN_PRINCIPLES.md)

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
    "story_role": "moment",
    "director_note": "Treat the lamp as a sign of care, not dramatic spectacle."
  }
}
```

- **Observation** records what is visibly present.
- **Interpretation** records a tentative theme and emotional reading.
- **Direction** records editable role and layout decisions.
- **Narrative Systems** decide how one image or a sequence can be read.

The distinction prevents inferred meaning from being presented as photographic fact. Automatic analysis remains conservative, and every Scene Card decision can be edited before prompt compilation.

## Current systems, Profiles, and deterministic typography

The compiler turns Scene Card evidence, one Narrative System, and one replaceable Expression Profile into a versioned JSON generation contract. Eleven Narrative Systems are supported. The system defines how the story is read; the Profile defines how that mechanism is visually expressed. `source-led` remains the default.

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
| `journey-taxonomy` | Journey Taxonomy | semantic groups of visible place evidence organized into one spatial field |
| `street-reportage` | Street Reportage | observed public gestures and factual sequence |
| `fashion-editorial` | Fashion Editorial | pose, garment construction, crop, shot-scale rhythm |

Nineteen replaceable Profiles are available beyond the default `source-led`. Eleven materially distinct additions expand the system beyond photography: mineral ink, impasto, authored pixel art, risograph, gouache, cyanotype, paper relief, early-color photography, pixel-and-ink fusion, a physically sculpted 3D diorama, and continuous threaded textile relief. `pixel-ink-memory` is explicitly experimental. The v0.3.3 name `full-watercolor-memory` remains a compatibility alias for `watercolor-chronicle` inside Memory Atlas and is not counted separately.

| Expression Profile | Compatible Narrative Systems |
| --- | --- |
| `source-led` | all systems |
| `rain-nocturne` | Cinematic Sequence |
| `quiet-window-light` | Quiet Editorial |
| `watercolor-contour` | Memory Atlas |
| `watercolor-chronicle` | Memory Atlas, Family Chronicle, Museum Catalogue, Travel Journal |
| `graphite-paper` | Family Chronicle |
| `heritage-portrait` | Family Chronicle, Museum Catalogue |
| `monochrome-reportage` | Street Reportage |
| `dream-logic` | Memory Atlas, Fashion Editorial |
| `mineral-ink-memory` | Memory Atlas, Travel Journal, Journey Taxonomy |
| `impasto-light-study` | Quiet Editorial, Memory Atlas, Travel Journal, Journey Taxonomy |
| `pixel-diary` | Memory Atlas, Travel Journal, Journey Taxonomy |
| `risograph-route` | Memory Atlas, Travel Journal, Journey Taxonomy |
| `gouache-place-study` | Memory Atlas, Travel Journal, Journey Taxonomy |
| `cyanotype-archive` | Field Log, Family Chronicle, Museum Catalogue, Street Reportage |
| `paper-relief-landscape` | Memory Atlas, Travel Journal, Journey Taxonomy |
| `autochrome-memory` | Memory Atlas, Family Chronicle, Travel Journal, Journey Taxonomy |
| `pixel-ink-memory` · experimental | Memory Atlas, Journey Taxonomy |
| `sculpted-place-diorama` · 3D | Memory Atlas, Travel Journal, Journey Taxonomy |
| `threaded-landscape` | Family Chronicle, Memory Atlas, Travel Journal, Journey Taxonomy |

### Journey Keepsake presentation

`Journey Keepsake` is a deterministic presentation mode, not another image style. It places one accepted After inside an original asymmetric collector sheet with a side provenance stub and only user-supplied captions, locations, dates, collection data, and notes:

```bash
scene-card-studio present render-manifest.json \
  --style journey-keepsake \
  --output journey-keepsake.svg
```

It does not generate a second image, change candidate pixels, reproduce an upper/lower comparison, or borrow sample slogans and layout proportions from a reference prompt.

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

Every prompt now carries a structured `output_contract` with exact MIME type, width, height, and aspect ratio. `bind-outputs` decodes the candidate and rejects format or dimension mismatches before review. Candidate paths are stored relative to the Render Manifest so bundles remain portable. Formal review reopens and re-hashes the current files; replacing an image after binding invalidates the review. Optional `reference_output` records are benchmark comparisons only: a formal review must target a Render Manifest containing `candidate_output` records.

Sequence systems additionally review subject continuity, light/color continuity, rhythm, and narrative arc. Retry provenance is a closed hash chain: Prompt Manifest → failed Render Manifest → failed Review → Retry Manifest → post-retry Render Manifest → accepted Review. Each link records its parent hash and chronology.

## Narrative Systems, not style filters

The project expands through recording and reading mechanisms, not a flat menu of visual effects. Watercolor, heritage photographic process, monochrome treatment, and dream logic remain replaceable Profiles. A system must explain what narrative work it performs; a list of aesthetic keywords is not enough.

## Quick start

Requires Python 3.10+. Automatic analysis and PNG rendering use Pillow.

```bash
git clone https://github.com/swping999/scene-card-studio.git
cd scene-card-studio
python -m pip install -e .

# Fast path: one photo → one prompt-ready local direction bundle
scene-card-studio direct photos/portrait.jpg --brief "quiet family portrait with restrained silver-gelatin depth"

# The local analyzer deliberately stops before inventing semantic evidence.
scene-card-studio check scene-card-output/story.json --json

# After a human or vision-capable Skill completes and verifies the Scene Cards:
scene-card-studio direct photos/portrait.jpg \
  --brief "quiet family portrait with restrained silver-gelatin depth" \
  --scene-cards scene-card-output/story.json --force

# Fast path: many photos → one automatically routed narrative bundle
scene-card-studio direct photos/*.jpg --brief "a travel journal built from stations, tickets, and thresholds" --output-dir travel-run

# Advanced staged workflow
scene-card-studio analyze photos/portrait.jpg --output portrait-story.json
# Complete the reported semantic fields from visual evidence before compiling for generation.
scene-card-studio check portrait-story.json --json
scene-card-studio profiles --system family-archive
scene-card-studio compile portrait-story.json --system family-archive --expression-profile heritage-portrait --output portrait-manifest.json

# Many photos → per-photo direction or multi-source synthesis
scene-card-studio analyze photos/*.jpg --output story.json
scene-card-studio check story.json --json
scene-card-studio recommend story.json
scene-card-studio compile story.json --system cinematic-storyboard --expression-profile source-led --output prompt-manifest.json
scene-card-studio compile story.json --system memory-atlas --expression-profile watercolor-chronicle --output watercolor-memory-manifest.json
scene-card-studio compile story.json --system museum-catalogue --expression-profile heritage-portrait --output catalogue-manifest.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio render story.json --style memory-atlas --format svg --output story.svg
scene-card-studio render story.json --style field-log --mode workprint --format png --output notes.png
scene-card-studio consent prompt-manifest.json --provider PROVIDER --purpose "presentation synthesis" --confirm --output upload-consent.json
scene-card-studio bind-outputs prompt-manifest.json --result cinematic-storyboard-01=after-01.png --output render-manifest.json
scene-card-studio review-template render-manifest.json --reviewer-type human --reviewer-name "YOUR NAME" --reviewer-model "visual inspection" --method "full-resolution comparison" --output assessment.json
# Fill every 1–5 score after inspecting the bound image, then finalize the record:
scene-card-studio review render-manifest.json assessment.json --output review.json
scene-card-studio present render-manifest.json --output presentation.svg
scene-card-studio retry render-manifest.json review.json --output retry-manifest.json
scene-card-studio bind-outputs retry-manifest.json --result cinematic-storyboard-01=after-01-retry.png --output post-retry-render-manifest.json
```

`direct` writes `story.json`, `prompt-manifest.json`, `workprint.svg`, and `run-summary.json` into a dedicated output directory. It refuses accidental overwrites unless `--force` is explicit. `check` reports the exact semantic fields that remain incomplete. A prepared story may re-enter the same flow through `--scene-cards`; its source list must match the supplied photos exactly, and low-level image measurements are refreshed from the files. For one photo, every system emits exactly one standalone prompt and labels the Manifest `single-photo`; no sequence continuity or invented adjacent scene is requested. For multiple photos, Cinematic, Quiet Editorial, Editorial Rhythm, Field Log, Museum, Street, and Fashion emit one prompt per source, while Memory Atlas, Family Chronicle, Travel Journal, and Journey Taxonomy emit one synthesis prompt.

Cloud synthesis requires explicit consent containing the provider, purpose, and exact upload list. Missing or incomplete direction-readiness evidence fails closed. Formal review refuses an unbound Prompt Manifest, and `retry` refuses an unfinished or accepted review. `present` verifies bound output hashes, writes portable relative image references, and keeps generated pixels separate from deterministic text. Raster analysis, output binding, and safe SVG embedding enforce source-byte and pixel limits.

The repository also includes a [bilingual routing matrix](evals/direct-briefs.json) with positive, negated, and ambiguous briefs. CI checks all eleven Narrative Systems, all non-default Profiles, single-photo contracts, multi-photo modes, semantic readiness, formal review, retry provenance, safe image embedding, recompilable gallery evidence, and pixel-level visual difference across every published Before/After pair.

## Codex Skill

The Codex Skill is included in both source checkouts and built wheels. Install it into a new Codex Skill directory, then restart Codex:

```bash
scene-card-studio skill-path
scene-card-studio install-skill --target ~/.codex/skills/scene-card-studio
```

The install command refuses to overwrite an existing Skill directory.

Then ask:

```text
Use $scene-card-studio to direct this photo as a quiet hand-colored heritage portrait.
```

The Skill uses the same local `direct` bundle first, completes semantic Scene Card evidence through visual inspection, verifies it with `check`, then asks for provider-, purpose-, and file-specific consent before any remote image generation.

## Originality and privacy

- no third-party style assets;
- no prompts copied from similarly themed repositories;
- repository examples use newly generated project-owned demo assets;
- the core contribution is the Scene Card + Visual Director + narrative rendering workflow;
- source photos stay local unless the user explicitly chooses otherwise.

See [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) for the versioned provenance record and [example asset terms](examples/ASSET_LICENSE.md) for per-asset licensing.

## Contributing and security

New Narrative Systems must introduce a distinct way of reading one photo or a photo sequence; new Expression Profiles must remain replaceable and may not imitate a named creator or reuse third-party visual assets. Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing either one.

Please report suspected path traversal, unintended photo disclosure, manifest spoofing, unsafe image handling, prompt injection, or credential exposure through the repository's private security-reporting channel. See [SECURITY.md](SECURITY.md).

## Roadmap

- richer semantic-image adapters beyond the bundled Skill workflow;
- `contact-sheet` and `journey-sequence` systems;
- crop-aware subject placement;
- image-model adapters and queued generation;
- printable PDF and social carousel renderers;
- browser preview and drag-to-reorder editor;
- community-authored Narrative Systems.

## License

Code and repository-specific demo assets are Apache-2.0; the bundled font remains under SIL OFL 1.1. See [example asset terms](examples/ASSET_LICENSE.md).

See [CHANGELOG.md](CHANGELOG.md) for release history.
