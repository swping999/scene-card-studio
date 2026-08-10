# Generative case record / 生成案例记录

Generated on 2026-08-09 with OpenAI's built-in image generation tool. All source photographs are fictional images generated specifically for this repository.

## Memory Atlas

- Sources: `photos/rain-greenhouse.png`, `photos/valley-fruit-stand.png`, `photos/coastal-platform.png`
- Scene Cards: `generated-story.json`
- Prompt Manifest: `prompt-manifest.json`
- Render Manifest: `render-manifest.json`
- Accepted Review: `accepted-review.json`
- After: `outputs/memory-atlas-ai-composite.png`
- Direction: preserve the three actual photographic buildings and integrate them into one hand-drawn mountain-to-coast geography using watercolor terrain, contour marks, archival paper, and subtle travel ephemera. No arrows, UI route lines, labels, or invented metadata.

## Family Archive

- Sources: `cases/family-archive/photos/`
- Scene Cards: `cases/family-archive/story.json`
- Prompt Manifest: `cases/family-archive/prompt-manifest.json`
- Render Manifest: `cases/family-archive/render-manifest.json`
- Accepted Review: `cases/family-archive/accepted-review.json`
- After: `cases/family-archive/outputs/family-archive-ai-composite.png`
- Direction: preserve fictional people, gestures, clothing, faces, and hands as documentary photography; integrate them with graphite studies of domestic objects, torn paper, contact-print edges, thread, and archival traces. No invented names or dates.

## Cinematic Storyboard

- Sources: `cases/cinematic-storyboard/photos/raw-bus-stop.png`, `raw-diner.png`, `raw-taxi.png`
- Scene Cards: `cases/cinematic-storyboard/story.json`
- Prompt Manifest: `cases/cinematic-storyboard/prompt-manifest.json`
- Accepted post-retry Render Manifest: `cases/cinematic-storyboard/retry-example/post-retry-render-manifest.json`
- Accepted Review: `cases/cinematic-storyboard/accepted-review.json`
- Failed → retry record: `cases/cinematic-storyboard/retry-example/`
- Afters: `cases/cinematic-storyboard/outputs/after-bus-stop.png`, `after-diner.png`, `after-taxi.png`
- Direction: transform three deliberately ordinary rainy-night phone snapshots into three separate film frames. Preserve the recognizable subject of each source; use weather, shot scale, mixed blue/amber light, reflection, and temporal continuity. No collage, split screen, titles, or director imitation.

## Minimal Editorial

- Sources: `cases/minimal-editorial/photos/raw-mug.png`, `raw-chair.png`, `raw-linen.png`
- Scene Cards: `cases/minimal-editorial/story.json`
- Prompt Manifest: `cases/minimal-editorial/prompt-manifest.json`
- Render Manifest: `cases/minimal-editorial/render-manifest.json`
- Accepted Review: `cases/minimal-editorial/accepted-review.json`
- Afters: `cases/minimal-editorial/outputs/after-mug.png`, `after-chair.png`, `after-linen.png`
- Direction: give each deliberately cluttered household snapshot its own quiet photographic stage. Preserve the recognizable object and material wear; remove accidental clutter and direct attention through natural light, shadow, negative space, and tactile texture. No collage, panels, typography, or abstract overlays.

The four Prompt Manifests record compiler version `0.3.2`, source hashes, complete modular prompts, expression profiles, benchmark references, and structured output contracts. Formal reviews target Render Manifests containing decoded and validated `candidate_output` metadata; benchmark `reference_output` records cannot satisfy review. Cinematic Storyboard includes the complete Prompt → failed render → failed review → retry → post-retry render → accepted review hash chain and sequence-level scores. PNG renderer outputs in adjacent folders are deterministic workprints. Files named `*-ai-composite.png` and the six `after-*.png` files above are presentation synthesis outputs. Asset provenance and usage terms are recorded in [`ASSET_LICENSE.md`](ASSET_LICENSE.md).

## v0.4 gallery · 13 fresh comparisons

Generated on 2026-08-10 with OpenAI's built-in image generation tool. This new gallery supplements rather than replaces the four benchmark cases above.

- Sources: `cases/v0.4-gallery/before/`
- Directed outputs: `cases/v0.4-gallery/after/`
- Scene Cards and transformation policies: `cases/v0.4-gallery/case-records.json`
- Case map and method note: `cases/v0.4-gallery/README.md`
- Coverage: Cinematic Sequence, Memory Atlas, Family Chronicle, Quiet Editorial, Editorial Rhythm, Field Log, Watercolor Chronicle, Heritage Portrait, Museum Catalogue, Travel Journal, Street Reportage, Fashion Editorial, and Dream Logic.
- Direction rule: every Before is a newly generated unpolished source; every After materially redirects the matching source while preserving the specified identity, object, gesture, clothing, or spatial evidence. Borders, grids, contact sheets, and decorative collages cannot count as the transformation.
- Originality rule: no third-party photograph, artwork, prompt, visual asset, living artist name, director name, photographer name, or publication name was used as a style reference.

The gallery records are compact example-level provenance and direction records. The original four benchmark cases remain the repository's complete hash-bound compile, bind, review, and retry demonstrations.
