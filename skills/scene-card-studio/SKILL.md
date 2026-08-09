---
name: scene-card-studio
description: Turn user-supplied photos into a coherent visual narrative, versioned image-generation prompts, art-directed Before/After images, and editable story layouts. Use when the user wants a photo essay, cinematic photo treatment, minimal editorial still life, family archive, travel memory map, visual journal, contact sheet, social carousel, micro-zine plan, or a sequenced photographic story.
---

# Scene Card Studio

Build a visual story from the user's photographs without imitating a named artist or copying a reference project's protected assets.

## Workflow

1. Treat only user-supplied photos as content sources. Keep them local during analysis, Scene Card authoring, compilation, and workprint rendering.
2. For every photo, create a Scene Card using `references/scene-card.md`. Keep observable evidence separate from interpretive direction.
3. Add a Visual Director decision: narrative intent, emotional tone, story role, concise director note, and confidence. Never present this interpretation as photographic fact.
4. Preserve the user's input order by default. Reorder only when the user requests it or explicitly approves `--reorder`; then use opening, development, pause, and closing roles.
5. Recommend one Narrative System with an explicit reason:
   - `editorial-sequence` for a quiet, flexible photo essay;
   - `family-archive` for repeated people, objects, or domestic gestures; use family relationships or inheritance only when the user supplies them;
   - `cinematic-storyboard` for temporal continuity, light progression, and shot relationships;
   - `minimal-editorial` for object hierarchy, negative space, geometry, and material rhythm;
   - `memory-atlas` when movement, route, distance, place, or spatial memory matters; do not assume a return;
   - `field-log` when observation and documentary detail matter.
6. Decide the output tier:
   - **Workprint**: use the deterministic renderer for analysis, sequencing, iteration, and editable layout.
   - **Presentation synthesis**: compile versioned prompts and use image generation to create a genuinely transformed artifact. Read `references/synthesis.md`, `references/prompt-compiler.md`, and `references/privacy.md`. Preserve recognizable photographic subjects; do not call a rearranged photo grid an After image.
7. Write the cards to `story.json`. When the package is installed, run:

```bash
scene-card-studio recommend story.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio compile story.json --system cinematic-storyboard --output prompt-manifest.json
```

8. Before any remote or cloud generation, show the user the provider, purpose, and exact `privacy.files` list. Ask for explicit consent and record it with `scene-card-studio consent`. Without consent, stop at local Workprint and Prompt Manifest output. Never treat photo analysis or prompt compilation as upload permission.
9. After consent, use every module in each compiled prompt and pass only the approved source photographs as image references. Default to **one source photograph → one standalone After image**. Combine sources only when explicitly requested or when spatial or archival synthesis requires it.
10. Bind generated files with `scene-card-studio bind-outputs`. Require the decoded MIME, width, height, and aspect ratio to match each `output_contract`; do not review mismatched files.
11. Review only `candidate_output` records in the Render Manifest. A `reference_output` is benchmark evidence and never satisfies formal review. For a cinematic sequence, also score identity continuity, light/color continuity, rhythm, and narrative arc. Accept only when every score is at least 4.
12. If a dimension fails, write the hash-bound assessment JSON, run `scene-card-studio retry`, regenerate only `retry_prompt_ids`, and bind all resulting candidates to the Retry Manifest. Accept only a review bound to this post-retry Render Manifest. Do not reuse the pre-retry review or candidates.
13. Return paired Before and After artifacts, Scene Cards, accepted Render Manifest, review record, and a short explanation. When several one-to-one transformations exist, show every pair separately.

## Guardrails

- Never invent names, places, dates, or events not supplied or visible.
- Keep faces and identity-bearing details truthful; do not reconstruct hidden content.
- Prefer omission and spacing over decorative filler.
- Use colors sampled from the photographs unless the user supplies a palette.
- Keep captions short and concrete. Mark uncertain interpretations as uncertain.
- Do not save source photos into a repository unless the user explicitly requests it.
- Do not imitate a living artist, photographer, or director by name. Translate requests into general visual and narrative mechanisms.

## Bundled resources

- Read `references/scene-card.md` before manually authoring or revising Scene Cards.
- Run `scripts/render_story.py` when the package is not installed but the repository source tree is available.
- Run `scripts/compile_prompt.py`, `scripts/bind_outputs.py`, and `scripts/retry_prompt.py` for versioned prompts, contract-checked output binding, and targeted retries when the package is not installed.
- Run `scripts/record_consent.py` only after the user explicitly approves the exact provider, purpose, and file list.
- Read `references/synthesis.md` whenever the user asks for an After image or finished visual artifact rather than a layout workprint.
- Read `references/prompt-compiler.md` whenever compiling, reviewing, retrying, or maintaining a Hero Case.
- Read `references/privacy.md` before any remote or cloud image generation.
