# Changelog

All notable changes to Scene Card Studio are documented here. Versions follow semantic versioning where practical; Prompt Manifest and Scene Card schemas retain their own explicit version numbers.

## [0.4.3] - 2026-08-31

### Added

- Explicit `single-photo`, `multi-photo-per-source`, and `multi-photo-synthesis` contracts in Prompt and Presentation Manifests.
- `scene-card-studio profiles` for discovering valid System/Profile combinations.
- Regression coverage for every Narrative System and compatible Profile in standalone single-photo mode.

### Fixed

- Single-photo analysis now assigns the standalone `moment` role instead of a sequence opening.
- Single-photo recommendations and compiled prompts no longer request other frames, chronology, routes, relatives, destinations, or sequence continuity.
- `--aspect-ratio source` now preserves the source orientation for one-photo synthesis-system prompts instead of applying the multi-photo 4:5 default.
- All 13 published one-photo gallery records now use the schema-valid standalone `moment` role, with regression checks that every Before and After exists and differs.
- CLI JSON and render commands now create missing output directories.

### Documented

- Complete compatibility tables for all eight replaceable Expression Profiles in both READMEs and the bundled Codex Skill.

## [0.4.2] - 2026-08-31

### Added

- A clearer bilingual repository landing section, project contract, navigation, and complete installation path.
- Contributor guidance with originality, privacy, testing, and asset-provenance requirements.
- A private security-reporting policy focused on photo disclosure, unsafe paths, manifest integrity, image embedding, prompt injection, and credentials.
- Structured GitHub issue forms, a pull-request checklist, and automated dependency updates.

### Changed

- Synchronized the package version with the public release line.
- Preserved the opening film, all 13 v0.4 gallery pairs, and the earlier benchmark evidence.

## [0.4.1] - 2026-08-10

- Added the complete visual-direction gallery with 13 distinct Before/After pairs.

## [0.4.0] - 2026-08-10

- Separated Narrative Systems from replaceable Expression Profiles.
- Added deterministic presentation contracts and expanded the system catalogue.

## [0.3.3] - 2026-08-10

- Added the full-frame watercolor chronicle profile.

## [0.3.2] - 2026-08-09

- Closed review, retry, image-contract, safe-embedding, schema-migration, and privacy-consent gaps.

## [0.3.1] - 2026-08-09

- Added continuous integration for supported Python versions.

[0.4.3]: https://github.com/swping999/scene-card-studio/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/swping999/scene-card-studio/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/swping999/scene-card-studio/releases/tag/v0.4.1
[0.4.0]: https://github.com/swping999/scene-card-studio/releases/tag/v0.4.0
[0.3.3]: https://github.com/swping999/scene-card-studio/releases/tag/v0.3.3
[0.3.2]: https://github.com/swping999/scene-card-studio/releases/tag/v0.3.2
[0.3.1]: https://github.com/swping999/scene-card-studio/releases/tag/v0.3.1
