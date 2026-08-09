# Failed → targeted retry → accepted

This example is a complete hash-linked retry record. The first candidate
deliberately uses the source bus-stop snapshot as if it were a finished render.
It preserves the subject, but fails narrative alignment, composition, and
system distinctiveness.

- `failed-render-manifest.json` links to the Prompt Manifest and binds all three
  Prompt IDs to exact candidate hashes and structured image metadata.
- `failed-review.json` links to that Render Manifest and rejects only
  `cinematic-storyboard-01`.
- `retry-manifest.json` links to both the failed Render Manifest and failed
  Review, removes stale candidates, and appends corrections only to that Prompt.
- `post-retry-render-manifest.json` links to the Retry Manifest and binds the
  corrected output plus the two unchanged accepted outputs.
- `../accepted-review.json` links to the post-retry Render Manifest and accepts
  the result after the failed review, including sequence-level scores.

The rejected candidate is `../photos/raw-bus-stop.png`; the corrected accepted
output is `../outputs/after-bus-stop.png`.
