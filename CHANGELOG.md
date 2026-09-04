# Changelog

All notable changes to Scene Card Studio are documented here. Versions follow semantic versioning where practical; Prompt Manifest and Scene Card schemas retain their own explicit version numbers.

## [0.7.0] - 2026-09-04

### Added

- v0.7 After-only Director Gallery with `travel-zine`, `chinese-photo-editorial`, `selective-material-relief`, and `chinese-ink-poetry` examples.
- `chinese-ink-poetry` expression profile and `ink-poetry` presentation style for Guofeng photo repainting with user-supplied verse overlay.
- Structured `expression_profile_tokens` in Prompt Manifests for composition, palette, texture, and typography decisions.
- Scene Card direction fields for negative space, text zone, typography orientation, material transition, and source-light/perspective preservation.

### Changed

- Public showcase guidance now leads with finished After images while retaining prior Before/After evidence cases.
- Bilingual routing recognizes the new travel, ink-editorial, and selective-relief vocabulary.

## [Unreleased]

### Added

- Semantic Scene Card readiness reports through `scene-card-studio check`.
- `--scene-cards` support for rerunning `direct` with visually inspected, source-matched semantic direction.
- Hash-bound `review-template` and `review` commands for a complete Accept/Retry path.
- Recompilable `story.json` and Prompt Manifest evidence for all 13 landing-page cases.
- Negation-aware routing and explicit confirmation when automatically recommended Systems tie or remain below the confidence threshold.
- Portable Render Manifest candidate paths plus `skill-path` and `install-skill` commands for the wheel-bundled Codex Skill.
- `Journey Taxonomy`, an original landscape-led Narrative System that organizes supplied place evidence by semantic role without copying a reference layout.
- Eleven material Expression Profiles: mineral ink, impasto, pixel diary, risograph, gouache, cyanotype, paper relief, autochrome, experimental pixel-and-ink, a physically sculpted 3D place diorama, and continuous threaded textile relief.
- A 12-case, landscape-first Before/After gallery with Scene Cards and recompilable Prompt Manifest evidence.
- `journey-keepsake`, an original asymmetric deterministic presentation style that uses one accepted After and supplied metadata without copying a reference prompt's split layout or slogans.

### Changed

- Prompt Manifest schema 1.5 records semantic readiness and route readiness separately.
- Upload consent now refuses incomplete semantic direction or an unresolved automatic route.
- Pillow is installed with the core package; package metadata and source-distribution boundaries are explicit.
- Review reopens the current candidate files, while Retry requires a finalized failed review and refuses accepted or unfinished assessments.

### Safety and reliability

- Prepared Scene Cards must match the supplied source files in the same order; low-level measurements are refreshed from those files.
- Reference After images remain benchmarks and cannot substitute for formally bound candidate outputs.
- Routing evaluations now include negated and ambiguous bilingual briefs.
- Routing evaluations cover every new system and material Profile in both English and Chinese.
- Story, candidate, and presentation references remain relative and do not emit local `file://` paths; raster analysis and output binding enforce byte and pixel limits.

## [0.5.0] - 2026-09-01

### Added

- `scene-card-studio direct` as a safe one-command local workflow for one photo or a related photo set.
- Automatic bilingual Narrative System routing from a user-supplied `--brief`.
- Conservative automatic Expression Profile selection: non-default Profiles require explicit visual-language cues; otherwise routing stays `source-led`.
- A portable Direct bundle containing Scene Cards, Prompt Manifest, analysis Workprint, and a machine-readable run summary.
- A 13-case bilingual routing evaluation matrix covering all ten Narrative Systems and every non-default Expression Profile.

### Changed

- Simplified the English and Chinese landing-page path without removing any Before/After or earlier benchmark case.
- Updated the bundled Codex Skill to begin with the local Direct bundle and continue to remote generation only after explicit upload consent.
- Improved recommendation vocabulary for cinematic, memory, family, editorial, field, museum, travel, street, fashion, and minimal requests in English and Chinese.

### Safety and reliability

- Direct runs refuse accidental overwrite unless `--force` is explicit and only replace their four known artifacts.
- Direct runs state that no photo was uploaded and that the Workprint is not a generated After.
- Heuristic default words no longer overpower an explicit user brief during routing.
- Published Before/After regression now measures pixel-level visual difference instead of relying only on unequal file hashes.

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

[0.5.0]: https://github.com/swping999/scene-card-studio/compare/v0.4.3...v0.5.0
[0.4.3]: https://github.com/swping999/scene-card-studio/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/swping999/scene-card-studio/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/swping999/scene-card-studio/releases/tag/v0.4.1
[0.4.0]: https://github.com/swping999/scene-card-studio/releases/tag/v0.4.0
[0.3.3]: https://github.com/swping999/scene-card-studio/releases/tag/v0.3.3
[0.3.2]: https://github.com/swping999/scene-card-studio/releases/tag/v0.3.2
[0.3.1]: https://github.com/swping999/scene-card-studio/releases/tag/v0.3.1
