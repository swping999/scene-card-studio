# Prompt Compiler and aesthetic review

Use the compiler for presentation-quality generation with any Narrative System listed in `systems-and-profiles.md`.

## Compile

```bash
scene-card-studio compile story.json \
  --system cinematic-storyboard \
  --expression-profile source-led \
  --output prompt-manifest.json
```

The Narrative System defines how the story is read. The replaceable Expression Profile defines the visual language. Do not treat profiles as additional Narrative Systems.

For `memory-atlas`, choose deliberately:

- `source-led` derives the visual language only from supplied evidence;
- `watercolor-contour` keeps people and places photographic while drawing the remembered geography around them;
- `watercolor-chronicle` repaints people, clothing, architecture, landscape, and spatial transitions in one continuous watercolor medium while preserving identity and source geometry.

`full-watercolor-memory` remains a compatibility alias. Prefer the canonical `watercolor-chronicle` name in new Manifests.

Do not provide a named artist or unlicensed artwork as a style reference for `watercolor-chronicle` or its compatibility alias.

Each prompt contains:

1. subject fidelity;
2. explicit `MUST PRESERVE / MAY TRANSFORM / MUST REMOVE` policy;
3. narrative intent;
4. composition;
5. lighting and color;
6. material and surface;
7. spatial relationships;
8. text and label strategy;
9. exclusions;
10. output contract and format.

With one Scene Card, every system emits exactly one standalone prompt, assigns `source_mode: single-photo`, and omits sequence continuity or invented adjacent scenes. With multiple Scene Cards, Cinematic Sequence, Quiet Editorial, Editorial Rhythm, Field Log, Museum Catalogue, Street Reportage, and Fashion Editorial emit one prompt per source and assign `multi-photo-per-source`; Memory Atlas, Family Chronicle, and Travel Journal emit one synthesis prompt and assign `multi-photo-synthesis`. Sequence systems include a shared continuity contract only when more than one source is present.

Every Manifest also includes a `presentation_contract`. Generated images must contain no visible typography. After binding candidate outputs, apply only supplied Scene Card metadata with:

```bash
scene-card-studio present render-manifest.json --output presentation.svg
```

Do not upload yet. Read `privacy.md`, show the exact provider, purpose, and `privacy.files`, obtain explicit consent, and record it. Then pass only approved source files and use every compiled module.

## Bind generated outputs

Bind each generated file to its prompt before review:

```bash
scene-card-studio bind-outputs prompt-manifest.json \
  --result cinematic-storyboard-01=outputs/frame-01.png \
  --output render-manifest.json
```

The compiler gives each Prompt a structured `output_contract` containing exact `mime_type`, `width`, `height`, and `aspect_ratio`. Binding fully decodes every candidate and rejects any mismatch. The Render Manifest records the validated metadata and output hash.

Review the Render Manifest, not an unbound Prompt Manifest. `reference_output` is optional benchmark comparison data only; formal review requires `candidate_output` for every Prompt.

## Review

Score every frame from 1 to 5 for:

- `subject_fidelity`;
- `narrative_alignment`;
- `composition`;
- `system_distinctiveness`;
- `artifact_control`.

When `sequence_review_required` is true, also score:

- `subject_continuity`;
- `light_color_continuity`;
- `rhythm`;
- `narrative_arc`.

Write a review bound to the exact Manifest and output hashes:

```json
{
  "schema_version": "1.0",
  "manifest_sha256": "SHA256 OF render-manifest.json",
  "reviewer": {
    "type": "model-assisted",
    "name": "reviewer name",
    "model": "model or human"
  },
  "reviewed_at": "2026-08-09T10:00:00Z",
  "review_method": "side-by-side visual inspection",
  "results": [
    {
      "prompt_id": "cinematic-storyboard-01",
      "output_sha256": "SHA256 OF REVIEWED OUTPUT",
      "scores": {
        "subject_fidelity": 5,
        "narrative_alignment": 4,
        "composition": 3,
        "system_distinctiveness": 4,
        "artifact_control": 5
      },
      "notes": "Strengthen the foreground and retain the original coat."
    }
  ],
  "sequence_scores": {
    "subject_continuity": 4,
    "light_color_continuity": 4,
    "rhythm": 4,
    "narrative_arc": 4
  }
}
```

Create the bound form rather than typing hashes by hand:

```bash
scene-card-studio review-template render-manifest.json \
  --reviewer-type human \
  --reviewer-name "REVIEWER" \
  --reviewer-model "visual inspection" \
  --method "full-resolution comparison" \
  --output assessment.json
```

After inspecting the candidate and filling every score, finalize it:

```bash
scene-card-studio review render-manifest.json assessment.json --output review.json
```

Every frame and sequence dimension must score at least 4. Mismatched Manifest or output hashes must fail review. The formal record adds `decision`, failed dimensions, and per-prompt decisions.

## Retry

```bash
scene-card-studio retry render-manifest.json review.json \
  --output retry-manifest.json
```

Use only `retry_prompt_ids` for the next generation pass. Preserve successful decisions and correct only failed frame or sequence dimensions. Then bind the corrected outputs and all accepted unchanged outputs to the Retry Manifest:

```bash
scene-card-studio bind-outputs retry-manifest.json \
  --result cinematic-storyboard-01=outputs/frame-01-retry.png \
  --result cinematic-storyboard-02=outputs/frame-02.png \
  --output post-retry-render-manifest.json
```

The Retry Manifest records the failed Render Manifest hash and failed Review hash. The post-retry Render Manifest records the Retry Manifest hash. The accepted Review must record the post-retry Render Manifest hash and have a later timestamp.

## Hero Case provenance

Maintain a Prompt Manifest, hash-bound Render Manifest, accepted review, and—where a retry occurs—the full failed Render → failed Review → Retry → post-retry Render → accepted Review chain. Compare narrative mechanism and fidelity rather than expecting pixel identity.
