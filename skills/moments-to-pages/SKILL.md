---
name: moments-to-pages
description: Turn one to twelve user-supplied photos into a coherent visual narrative and editable SVG story layout. Use when the user wants a photo essay, travel diary, contact sheet, visual journal, social carousel, micro-zine plan, or a sequence of photographs organized into opening, development, pause, and closing roles.
---

# Moments to Pages

Build a visual story from the user's photographs without imitating a named artist or copying a reference project's protected assets.

## Workflow

1. Treat only user-supplied photos as content sources. Do not browse for or upload private photos.
2. For every photo, create a Scene Card using `references/scene-card.md`.
3. Preserve chronology when it is meaningful. Otherwise order frames into opening, development, pause, and closing using contrast, visual energy, and subject continuity.
4. Choose one system:
   - `editorial-minimal` for a quiet, flexible photo essay;
   - `memory-map` when movement, route, distance, or return matters;
   - `field-notes` when observation and documentary detail matter.
5. Write the cards to `story.json`. When the package is installed, run:

```bash
moments-to-pages render story.json --style editorial-minimal --output story.svg
```

6. Inspect the SVG. Check photo order, crop safety, caption accuracy, contrast, and whether every decorative element performs a narrative function.
7. Return the editable SVG and a short explanation of the sequence. Generate bitmap or PDF derivatives only when the user requests them.

## Guardrails

- Never invent names, places, dates, or events not supplied or visible.
- Keep faces and identity-bearing details truthful; do not reconstruct hidden content.
- Prefer omission and spacing over decorative filler.
- Use colors sampled from the photographs unless the user supplies a palette.
- Keep captions short and concrete. Mark uncertain interpretations as uncertain.
- Do not save source photos into a repository unless the user explicitly requests it.

## Bundled resources

- Read `references/scene-card.md` before manually authoring or revising Scene Cards.
- Run `scripts/render_story.py` when the package is not installed but the repository source tree is available.
