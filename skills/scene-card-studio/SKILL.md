---
name: scene-card-studio
description: Turn one user-supplied photo or a related photo set into art-directed After images, coherent visual narratives, versioned prompts, and editable story layouts. Use for cinematic, memory, archive, editorial, travel, reportage, museum, watercolor, heritage, ink, relief, textile, pixel, risograph, gouache, or 3D treatments.
---

# Scene Card Studio

Build a visual story from the user's photographs without imitating a named artist or copying a reference project's protected assets.

## Workflow

1. Treat only user-supplied photos as content sources. Keep them local during analysis, Scene Card authoring, compilation, and workprint rendering.
2. For every photo, create a Scene Card using `references/scene-card.md`. Keep observable evidence separate from interpretive direction.
3. Add a Visual Director decision: narrative intent, emotional tone, story role, concise director note, and confidence. Never present this interpretation as photographic fact.
4. Preserve the user's input order by default. Reorder only when the user requests it or explicitly approves `--reorder`; then use opening, development, pause, and closing roles.
5. Read `references/systems-and-profiles.md`, then recommend one Narrative System with an explicit reason. Keep Narrative Systems separate from Expression Profiles:
   - `editorial-sequence` for a quiet, flexible photo essay;
   - `family-archive` for repeated people, objects, or domestic gestures; use family relationships or inheritance only when the user supplies them;
   - `cinematic-storyboard` for temporal continuity, light progression, and shot relationships;
   - `minimal-editorial` for object hierarchy, negative space, geometry, and material rhythm;
   - `memory-atlas` when movement, route, distance, place, or spatial memory matters; do not assume a return. Use `watercolor-contour` to retain photographic anchors or `watercolor-chronicle` to repaint people and places together as one watercolor medium;
   - `field-log` when observation and documentary detail matter.
   - `museum-catalogue` for inspectable subjects and supplied collection metadata;
   - `travel-journal` for movement, pauses, thresholds, and user-supplied journey evidence;
   - `journey-taxonomy` when the goal is to classify visible place elements by semantic role. Keep one dominant place image, omit absent categories, use no duplicated inset photo, sticker column, connector line, or copied reference composition;
   - `street-reportage` for observed public gestures and environmental context;
   - `fashion-editorial` for pose, garment construction, movement, and shot-scale rhythm.
   - v0.7 profiles add `travel-zine` (restrained source-bound travel page), `chinese-photo-editorial` (contemporary ink-and-paper photo treatment without invented motifs), and `selective-material-relief` (real photographic subject with an environment-only relief transformation). `chinese-ink-poetry` is the explicit general-purpose Guofeng option for people, pets, landscapes, architecture, interiors, vehicles, and objects: keep the real subject and original setting photographic, dissolve only source-derived peripheral regions into ink/paper, and place only the user's supplied poem or caption in the deterministic typography layer. These are visual expression profiles, not new Narrative Systems.
   Run `scene-card-studio profiles --system SYSTEM_ID` when available, and use only a Profile listed for the selected system. If the user explicitly delegates the visual choice, select the compatible Profile whose transformation rule best fits the visible evidence and requested outcome, explain the choice in one sentence, and prefer `source-led` when no non-default Profile has a clear evidence-based advantage.
6. Choose the source mode before choosing the output tier:
   - **Single-photo mode**: select one compatible Narrative System and Expression Profile, then produce exactly one standalone After for the supplied Before. Do not require a sequence and do not substitute a border, contact sheet, page mockup, or decorative collage for transformation.
   - **Multi-photo per-source mode**: direct every source as its own standalone After while preserving identity and sequence continuity where relevant.
   - **Multi-photo synthesis mode**: combine sources only when the user requests it or when the selected spatial, archival, or journey mechanism genuinely requires shared composition.
7. Decide the output tier:
   - **Workprint**: use the deterministic renderer for analysis, sequencing, iteration, and editable layout.
   - **Presentation synthesis**: compile versioned prompts and use image generation to create a genuinely transformed artifact. Read `references/synthesis.md`, `references/prompt-compiler.md`, and `references/privacy.md`. Preserve recognizable photographic subjects; do not call a rearranged photo grid an After image.
8. For a new request, prefer the one-command local preparation path when the package is installed. Pass the user's own words through `--brief`; use `--system` or `--expression-profile` when the user explicitly selects one or has explicitly delegated that choice and you have inspected the sources:

```bash
scene-card-studio direct PHOTO [PHOTO ...] --brief "USER-SUPPLIED DIRECTION" --output-dir scene-card-output
```

   Inspect `story.json`, `prompt-manifest.json`, `workprint.svg`, and `run-summary.json` before generation. The local analyzer provides only dimensions, orientation, palette, brightness, and saturation; never treat its empty or placeholder semantic fields as visual understanding. Inspect every supplied image, then complete `observation.subjects`, `observation.dominant_gesture`, `interpretation.narrative_intent`, `direction.director_note`, `direction.layout_emphasis`, `transformation.must_preserve`, and `transformation.may_transform` from visible evidence and the user's request. Run:

```bash
scene-card-studio check scene-card-output/story.json --json
scene-card-studio direct PHOTO [PHOTO ...] --brief "USER-SUPPLIED DIRECTION" \
  --scene-cards scene-card-output/story.json --output-dir scene-card-output --force
```

   Continue only when `check` reports `generation-ready` and the rerun reports `prompt-ready`. If two Narrative Systems tie or the automatic System score is low, `direct` reports `needs-route-confirmation`; resolve the system with the user or an explicit `--system`. `direct` may automatically select a non-default Profile only when the brief explicitly requests that expression; otherwise it must remain `source-led`. When the user explicitly delegates Profile choice, inspect the source, choose with the rule in step 5, and pass that Profile through `--expression-profile`. The Workprint is an analysis artifact, never the finished After. If staged control is required, run:

```bash
scene-card-studio recommend story.json
scene-card-studio profiles --system cinematic-storyboard
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio compile story.json --system cinematic-storyboard --output prompt-manifest.json
```

9. Before any remote or cloud generation, show the user the provider, purpose, and exact `privacy.files` list. Ask for explicit consent and record it with `scene-card-studio consent`. The command must refuse a Manifest whose semantic direction or route is not ready. Without consent, stop at the local Direct bundle or staged Workprint and Prompt Manifest output. Never treat photo analysis, automatic routing, or prompt compilation as upload permission.
10. After consent, use every module in each compiled prompt and pass only the approved source photographs as image references. Default to **one source photograph → one standalone After image**. Combine sources only when explicitly requested or when spatial or archival synthesis requires it.
   For medium-led Profiles, verify that the entire visible image follows one material system. Reject photo-plus-border effects, photographic islands inside full-redraw Profiles, inconsistent pixel scales, fake archive labels, and decorative route marks unsupported by Scene Cards.
11. Bind generated files with `scene-card-studio bind-outputs`. Require the decoded MIME, width, height, and aspect ratio to match each `output_contract`; do not review mismatched files.
12. Keep visible text out of image synthesis. Put only user-supplied `metadata` values into the Manifest's `presentation_contract`, then run `scene-card-studio present render-manifest.json -o presentation.svg` to apply deterministic captions, dates, places, collection names, and catalogue identifiers. For an original asymmetric travel-collectible layout, add `--style journey-keepsake`; it must present the generated After as the dominant image, never recreate a reference's upper/lower comparison, sample slogans, ticket proportions, or decorative arrangement. Omit missing fields instead of inventing them.
13. Review only `candidate_output` records in the Render Manifest. A `reference_output` is benchmark evidence and never satisfies formal review. Create a bound form with `scene-card-studio review-template`, inspect the full-resolution output, fill every score, then run `scene-card-studio review` to produce the formal Accept/Retry record. For sequence systems, also score identity continuity, light/color continuity, rhythm, and narrative arc. Accept only when every score is at least 4.
14. If a dimension fails, pass the finalized hash-bound review to `scene-card-studio retry`, regenerate only `retry_prompt_ids`, and bind all resulting candidates to the Retry Manifest. Accept only a new `scene-card-studio review` record bound to this post-retry Render Manifest. Do not reuse the pre-retry review or candidates.
15. For a public showcase, show the finished After image first and do not require a Before/After split. Keep paired source/After artifacts, Scene Cards, manifests, and review records in the reproducibility bundle when needed; never delete prior Before/After evidence cases.

## Guardrails

- Never invent names, places, dates, or events not supplied or visible.
- Keep faces and identity-bearing details truthful; do not reconstruct hidden content.
- Prefer omission and spacing over decorative filler.
- Use colors sampled from the photographs unless the user supplies a palette.
- Keep captions short and concrete. Mark uncertain interpretations as uncertain.
- Do not save source photos into a repository unless the user explicitly requests it.
- Do not imitate a living artist, photographer, or director by name. Translate requests into general visual and narrative mechanisms.
- Borrow only general mechanisms such as classification, sequencing, or material translation. Never copy another project's palette, composition, sticker silhouettes, caption placement, prompts, assets, or example arrangement.

## Bundled resources

- Read `references/scene-card.md` before manually authoring or revising Scene Cards.
- Run `scripts/render_story.py` when the package is not installed but the repository source tree is available.
- Run `scripts/compile_prompt.py`, `scripts/bind_outputs.py`, and `scripts/retry_prompt.py` for versioned prompts, contract-checked output binding, and targeted retries when the package is not installed.
- Run `scripts/record_consent.py` only after the user explicitly approves the exact provider, purpose, and file list.
- Read `references/synthesis.md` whenever the user asks for an After image or finished visual artifact rather than a layout workprint.
- Read `references/prompt-compiler.md` whenever compiling, reviewing, retrying, or maintaining a Hero Case.
- Read `references/privacy.md` before any remote or cloud image generation.
- Read `references/systems-and-profiles.md` when selecting, adding, or explaining a Narrative System or Expression Profile.
