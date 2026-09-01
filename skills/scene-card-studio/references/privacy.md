# Upload consent

Keep analysis, Scene Cards, prompt compilation, and workprint rendering local by default.

Before sending any source photograph to a remote or cloud image-generation provider:

1. Run `scene-card-studio check story.json` and require `generation-ready`; then compile the Prompt Manifest and require `generation_ready: true` with no unresolved route tie.
2. Tell the user the exact provider, purpose, and `privacy.files` list, including every path.
3. Ask for explicit consent to upload those files to that provider for that purpose.
4. Continue only after the user clearly agrees.
5. Record the approved scope:

```bash
scene-card-studio consent prompt-manifest.json \
  --provider "PROVIDER NAME" \
  --purpose "presentation synthesis" \
  --confirm \
  --output upload-consent.json
```

Do not infer consent from a request to analyze, arrange, compile, or render photos. Do not reuse consent for another provider, purpose, manifest, or file list. The consent command must refuse incomplete semantic direction. If the user does not consent, return only local Scene Cards, Prompt Manifest, and Workprint artifacts.
