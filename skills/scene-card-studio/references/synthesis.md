# Presentation synthesis

An After image must change the visual narrative, not merely place the same photos in a new grid.

## Default output contract

- One source photograph produces one standalone After image.
- Do not combine unrelated sources into collages, multi-panel boards, split screens, or designed pages merely to show several examples at once.
- Multiple photographs may share a sequence and visual direction while remaining separate outputs.
- Combine sources only when the user explicitly asks for a montage or the selected Narrative System depends on spatial synthesis, such as a Memory Atlas.

## Required sequence

1. Build Scene Cards and identify evidence that must remain faithful.
2. Select one Narrative System and describe its expressive mechanism.
3. Compile the Scene Cards with `scene-card-studio compile`; do not replace the manifest with improvised style keywords.
4. If synthesis uses a cloud or remote provider, disclose the provider, purpose, and exact source-file list; obtain explicit user approval and save it with `scene-card-studio consent`. Without approval, stop at the local Workprint and Prompt Manifest.
5. Pass only the approved files as image references and use all compiled prompt modules.
6. Bind every generated file to its Prompt ID with `scene-card-studio bind-outputs`; reject candidates whose decoded MIME, dimensions, or aspect ratio violate `output_contract`.
7. Inspect each frame with the five-dimension rubric in `prompt-compiler.md`; for sequence systems, also inspect subject continuity, light/color continuity, rhythm, and narrative arc.
8. Review only bound `candidate_output` records; never treat benchmark `reference_output` as a reviewed candidate.
9. Accept every prompt that passes. For failures, create a hash-bound assessment, run `scene-card-studio retry`, regenerate only `retry_prompt_ids`, bind the post-retry candidates to the Retry Manifest, and review that new Render Manifest.
10. Keep generated pixels free of visible text. After review, use `scene-card-studio present` to apply only supplied metadata through the deterministic overlay renderer.

## Memory Atlas

- With `source-led` or `watercolor-contour`, keep actual people, buildings, and places as photographic fragments and draw the remembered geography between them.
- With `watercolor-chronicle`, repaint faces, skin, hair, clothing, buildings, landscape, and geography in one continuous watercolor medium. Preserve identity, pose, anatomy, architecture, horizon, light direction, and source order. `full-watercolor-memory` is only a compatibility alias for older Memory Atlas Manifests.
- For full watercolor, reject any result that retains photographic pixels, pasted cutout edges, synthetic skin, or a photo-plus-watercolor-border appearance.
- Use transparent washes, paper tooth, restrained wet-on-wet diffusion, and selective dry-brush detail as general medium properties; do not imitate a named artist.
- Avoid arrows, digital route lines, flowcharts, and generic map pins.

## Family Archive

- Keep people, gestures, faces, hands, and clothing photographic.
- Use object studies, tracing paper, contact-print edges, fabric, domestic tools, photo corners, and restrained handwritten marks as the archive layer.
- Do not invent names, dates, or family relationships not supplied by the user.

## Cinematic Storyboard

- Keep people, locations, vehicles, and actions photographic.
- Render each source as a separate continuous photographic scene.
- Use cropping, shot scale, light continuity, weather, grain, and reflection to create temporal progression across outputs.
- Avoid fake titles, credits, dialogue, named-director imitation, equal-frame grids, and multi-shot composites.

## Minimal Editorial

- Keep object surfaces, wear, and material texture photographic.
- Give each source object its own continuous photographic scene.
- Remove accidental clutter and build hierarchy through scale, negative space, light, shadow, and material rhythm.
- Avoid decorative prop styling, abstract overlays, fake magazine mastheads, generic luxury branding, and multi-object collages.

## Museum, Travel, Street, and Fashion

- Museum Catalogue: create inspectable one-source plates; never invent provenance, period, maker, value, collection, or accession data.
- Travel Journal: synthesize only supplied movement, thresholds, tickets, places, and pauses; never invent dates, routes, or destinations.
- Street Reportage: preserve observed public gestures, body count, and event context; never stage urgency or sensationalize subjects.
- Fashion Editorial: preserve identity, anatomy, garment construction, accessories, and fabric behavior while using shot scale and crop rhythm.
- For all four, generate no visible captions, dates, places, catalogue numbers, mastheads, or brands. Add supplied metadata later with the deterministic renderer.

## Delivery

Return paired Before and After images, an optional Before contact sheet, the Scene Card JSON, Prompt Manifest, accepted Render Manifest, and accepted Review. Label deterministic layouts as `workprint`; reserve `After` for transformed presentation artifacts.
