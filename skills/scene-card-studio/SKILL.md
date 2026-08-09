---
name: scene-card-studio
description: Turn user-supplied photos into a coherent visual narrative, versioned image-generation prompts, art-directed Before/After images, and editable story layouts. Use when the user wants a photo essay, cinematic photo treatment, minimal editorial still life, family archive, travel memory map, visual journal, contact sheet, social carousel, micro-zine plan, or a sequenced photographic story.
---

# Scene Card Studio

Build a visual story from the user's photographs without imitating a named artist or copying a reference project's protected assets.

## Workflow

1. Treat only user-supplied photos as content sources. Do not browse for or upload private photos.
2. For every photo, create a Scene Card using `references/scene-card.md`. Keep observable evidence separate from interpretive direction.
3. Add a Visual Director decision: narrative intent, emotional tone, story role, concise director note, and confidence. Never present this interpretation as photographic fact.
4. Preserve the user's input order by default. Reorder only when the user requests it or explicitly approves `--reorder`; then use opening, development, pause, and closing roles.
5. Recommend one Narrative System with an explicit reason:
   - `editorial-sequence` for a quiet, flexible photo essay;
   - `family-archive` for recurring gestures, inheritance, and domestic memory;
   - `cinematic-storyboard` for temporal continuity, light progression, and shot relationships;
   - `minimal-editorial` for object hierarchy, negative space, geometry, and material rhythm;
   - `memory-atlas` when movement, route, distance, or return matters;
   - `field-log` when observation and documentary detail matter.
6. Decide the output tier:
   - **Workprint**: use the deterministic renderer for analysis, sequencing, iteration, and editable layout.
   - **Presentation synthesis**: compile versioned prompts and use image generation to create a genuinely transformed artifact. Read `references/synthesis.md` and `references/prompt-compiler.md`. Preserve recognizable photographic subjects; do not call a rearranged photo grid an After image.
7. Write the cards to `story.json`. When the package is installed, run:

```bash
scene-card-studio recommend story.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio compile story.json --system cinematic-storyboard --output prompt-manifest.json
```

8. For presentation synthesis, use every module in each compiled prompt and pass the listed source photographs as image references. Default to **one source photograph → one standalone After image**. Do not merge several photographs into a collage, multi-panel board, split screen, or designed page merely to demonstrate variety. Combine sources only when the user explicitly requests montage or when the chosen system requires spatial or archival synthesis.
9. Inspect the output with the five-dimension rubric in `references/prompt-compiler.md`. Score subject fidelity, narrative alignment, composition, system distinctiveness, and artifact control. Accept only when every score is at least 4.
10. If a dimension fails, write the assessment JSON, run `scene-card-studio retry`, and regenerate only the prompts in `retry_prompt_ids`. Do not rewrite successful prompt modules.
11. Return paired Before and After artifacts, the Scene Cards, the accepted prompt manifest, and a short explanation of the direction and sequence. When several one-to-one transformations exist, show every pair separately.

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
- Run `scripts/compile_prompt.py` and `scripts/retry_prompt.py` for versioned prompts and targeted retries when the package is not installed.
- Read `references/synthesis.md` whenever the user asks for an After image or finished visual artifact rather than a layout workprint.
- Read `references/prompt-compiler.md` whenever compiling, reviewing, retrying, or maintaining a Hero Case.
