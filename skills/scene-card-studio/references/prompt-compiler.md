# Prompt Compiler and aesthetic review

Use the compiler for presentation-quality image generation with `cinematic-storyboard`, `minimal-editorial`, `memory-atlas`, or `family-archive`.

## Compile

```bash
scene-card-studio compile story.json \
  --system cinematic-storyboard \
  --output prompt-manifest.json
```

The manifest is the generation contract. Each prompt contains these fixed modules:

1. subject fidelity;
2. narrative intent;
3. composition;
4. lighting and color;
5. material and surface;
6. spatial relationships;
7. text and label strategy;
8. exclusions;
9. output ratio and format.

For `cinematic-storyboard` and `minimal-editorial`, the compiler emits one prompt per source photograph. For `memory-atlas` and `family-archive`, it emits one multi-source synthesis prompt because spatial or archival relationships are the expressive mechanism.

Pass every `sources[].path` as an image reference and use `compiled_prompt` without silently dropping modules. Do not substitute a short list of style adjectives.

## Review

Inspect each result visually and score all five dimensions from 1 to 5:

- `subject_fidelity`;
- `narrative_alignment`;
- `composition`;
- `system_distinctiveness`;
- `artifact_control`.

Write an assessment matching this schema:

```json
{
  "results": [
    {
      "prompt_id": "cinematic-storyboard-01",
      "scores": {
        "subject_fidelity": 5,
        "narrative_alignment": 4,
        "composition": 3,
        "system_distinctiveness": 4,
        "artifact_control": 5
      },
      "notes": "Strengthen the foreground and retain the original coat."
    }
  ]
}
```

Every dimension must score at least 4. `subject_fidelity` and `artifact_control` are hard gates. Generate targeted retry prompts with:

```bash
scene-card-studio retry prompt-manifest.json assessment.json \
  --output retry-manifest.json
```

Use only prompts listed in `retry_prompt_ids` for the next generation pass. The retry prompt preserves successful decisions and adds corrections only for failed dimensions. Reinspect the new image before acceptance.

## Benchmark manifests

When maintaining a Hero Case, pass each accepted result with `--reference-output`. The compiler records source and output hashes with its versioned prompt. Use the reference output to judge narrative mechanism and fidelity, not pixel identity.
