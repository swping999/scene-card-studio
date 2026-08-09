# Failed → targeted retry → accepted

This example proves that review decisions are bound to a concrete Manifest and
concrete output bytes. The first candidate deliberately uses the untouched bus
stop source as if it were a finished render. It preserves the subject, but it
fails narrative alignment, composition, and system distinctiveness.

- `failed-render-manifest.json` binds all three Prompt IDs to exact output hashes.
- `failed-review.json` rejects only `cinematic-storyboard-01`.
- `retry-manifest.json` appends targeted corrections only to that Prompt and
  lists only that ID in `retry_prompt_ids`.
- `../accepted-review.json` binds and accepts the corrected three-frame result,
  including sequence-level continuity, rhythm, and narrative-arc scores.

The rejected candidate is `../photos/raw-bus-stop.png`; the corrected accepted
output is `../outputs/after-bus-stop.png`.
