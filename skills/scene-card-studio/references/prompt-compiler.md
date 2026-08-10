# Prompt Compiler and aesthetic review

Use the compiler for presentation-quality generation with `cinematic-storyboard`, `minimal-editorial`, `memory-atlas`, or `family-archive`.

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
- `full-watercolor-memory` repaints people, clothing, architecture, landscape, and spatial transitions in one continuous watercolor medium while preserving identity and source geometry.

Do not provide a named artist or unlicensed artwork as a style reference for `full-watercolor-memory`.

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

For cinematic and minimal systems, the compiler emits one prompt per source. For memory and archive systems, it emits one multi-source synthesis prompt. A cinematic manifest also includes one shared sequence contract.

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

For cinematic sequences, also score:

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

Every frame and sequence dimension must score at least 4. Mismatched Manifest or output hashes must fail review.

## Retry

```bash
scene-card-studio retry render-manifest.json assessment.json \
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
