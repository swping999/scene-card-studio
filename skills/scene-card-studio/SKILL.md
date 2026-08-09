---
name: scene-card-studio
description: Turn a set of user-supplied photos into a coherent visual narrative and editable story layout. Use when the user wants a photo essay, family archive, travel diary, contact sheet, visual journal, social carousel, micro-zine plan, or a sequence of photographs organized into opening, development, pause, and closing roles.
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
   - **Presentation synthesis**: use image generation to create a genuinely transformed mixed-media artifact. Read `references/synthesis.md` before prompting. Preserve recognizable photographic subjects; do not call a rearranged photo grid an After image.
7. Write the cards to `story.json`. When the package is installed, run:

```bash
scene-card-studio recommend story.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
```

8. For presentation synthesis, pass the source photographs as image references and translate Scene Card decisions into image instructions. Default to **one source photograph → one standalone After image**. Do not merge several photographs into a collage, multi-panel board, split screen, or designed page merely to demonstrate variety. Combine sources only when the user explicitly requests montage or when the chosen system requires spatial synthesis. For `memory-atlas`, keep real buildings photographic while drawing the geography between them. For `family-archive`, keep people photographic while layering object sketches, paper traces, and archival material.
9. Inspect the output. Check subject fidelity, photo order, crop safety, caption accuracy, contrast, and whether every element performs a narrative function.
10. Return paired Before and After artifacts plus a short explanation of the direction and sequence. When several one-to-one transformations exist, show every pair separately.

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
- Read `references/synthesis.md` whenever the user asks for an After image or finished visual artifact rather than a layout workprint.
