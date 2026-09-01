# Contributing to Scene Card Studio

Thank you for helping improve Scene Card Studio. Contributions should strengthen the project as a visual-narrative system rather than turn it into a collection of unrelated style presets.

## Development setup

Scene Card Studio requires Python 3.10 or newer.

```bash
git clone https://github.com/swping999/scene-card-studio.git
cd scene-card-studio
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest -q
```

## What belongs in the project

A **Narrative System** defines how supplied photographs are read together: through time, place, evidence, material hierarchy, public observation, or another explicit narrative relationship.

An **Expression Profile** defines a replaceable visual treatment. It must preserve the selected Narrative System's reading mechanism and subject-fidelity requirements.

Before proposing either one, answer:

1. What narrative or expressive problem does it solve?
2. Which Scene Card fields influence its decisions?
3. How does it differ structurally from an existing system or profile?
4. What must be preserved, may be transformed, and must be removed?
5. How can its behavior be tested without relying only on aesthetic adjectives?

## Originality requirements

- Do not copy prompts, prose, schemas, palettes, example compositions, or visual assets from another repository.
- Do not imitate a named living artist, photographer, filmmaker, studio, or publication.
- Use general visual mechanisms such as sequencing, contrast, negative space, material process, or shot relationships.
- Use only project-owned, contributor-owned, properly licensed, or explicitly authorized assets.
- Document the origin and license of every contributed example asset.
- Do not use a third-party artwork as a repository example or template, even when it has been modified.

Studying a problem category or a common design convention is acceptable. Reconstructing another project's distinctive selection, wording, parameter set, or arrangement is not.

## Privacy and safety

- Never commit private user photographs, credentials, API keys, access tokens, local paths containing personal information, or cloud-consent records from real users.
- Keep analysis and workprint generation local by default.
- Any remote-generation feature must enumerate the provider, purpose, and exact upload list and require explicit user consent.
- Treat captions, metadata, filenames, manifests, and imported Scene Cards as untrusted input.
- Do not add shell execution or unrestricted network access to the core workflow without a documented security review.

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

Changes to automatic routing must update `evals/direct-briefs.json` when they add or alter a supported user intent. The matrix must continue to cover every Narrative System and every non-default Expression Profile through representative English and Chinese briefs. New `direct` behavior must remain local-only until the existing explicit-consent step.

## Pull requests

Keep pull requests focused and include:

- the user problem and design rationale;
- tests for new behavior and failure modes;
- updated English and Chinese documentation when user-facing behavior changes;
- provenance and licensing for new assets;
- Before/After evidence for a new system or profile;
- confirmation that no secrets or private source photos are included.

By contributing, you agree that code and repository-specific assets you submit may be distributed under the licenses documented by this repository.
