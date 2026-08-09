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
10. output ratio and format.

For cinematic and minimal systems, the compiler emits one prompt per source. For memory and archive systems, it emits one multi-source synthesis prompt. A cinematic manifest also includes one shared sequence contract.

Do not upload yet. Read `privacy.md`, show the exact provider, purpose, and `privacy.files`, obtain explicit consent, and record it. Then pass only approved source files and use every compiled module.

## Bind generated outputs

Bind each generated file to its prompt before review:

```bash
scene-card-studio bind-outputs prompt-manifest.json \
  --result cinematic-storyboard-01=outputs/frame-01.png \
  --output render-manifest.json
```

The Render Manifest records each output hash. Review the Render Manifest, not an unbound Prompt Manifest.

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

Use only `retry_prompt_ids` for the next generation pass. Preserve successful decisions and correct only failed frame or sequence dimensions. Bind and review the new outputs again before acceptance.

## Hero Case provenance

Maintain a Prompt Manifest, hash-bound Render Manifest, accepted review, and—where available—a failed review plus retry manifest. Compare narrative mechanism and fidelity rather than expecting pixel identity.
