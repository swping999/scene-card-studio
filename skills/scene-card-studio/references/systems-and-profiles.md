# Systems and Profiles

Choose a Narrative System for how the photographs are read. Choose an Expression Profile for how that system is visually expressed. Never present the combined list as interchangeable filters.

## Narrative Systems

| ID | Display name | Narrative mechanism |
| --- | --- | --- |
| `cinematic-storyboard` | Cinematic Sequence | temporal continuity, motivated light, and shot relationships |
| `memory-atlas` | Memory Atlas | place, distance, direction, and spatial memory |
| `family-archive` | Family Chronicle | repeated supplied people, objects, gestures, and time |
| `minimal-editorial` | Quiet Editorial | object hierarchy, negative space, light, and material rhythm |
| `editorial-sequence` | Editorial Rhythm | sequencing, scale, contrast, density, and pause |
| `field-log` | Field Log | observed evidence, context, and documentary detail |
| `museum-catalogue` | Museum Catalogue | inspectable plates and supplied collection metadata |
| `travel-journal` | Travel Journal | movement, pauses, thresholds, and supplied journey evidence |
| `street-reportage` | Street Reportage | observed public gestures, event context, and factual sequence |
| `fashion-editorial` | Fashion Editorial | pose, garment construction, movement, crop, and shot-scale rhythm |

## Expression Profiles

- `watercolor-chronicle`: repaint every visible person, object, and place in one watercolor medium while preserving identity and geometry. Available for Memory Atlas, Family Chronicle, Museum Catalogue, and Travel Journal. Keep `full-watercolor-memory` as a Memory Atlas compatibility alias.
- `heritage-portrait`: use restrained silver-gelatin tonality and hand coloring without inventing period costume, ancestry, status, or age. Available for Family Chronicle and Museum Catalogue.
- `dream-logic`: apply one identity-locked impossible spatial rule without random collage. Available for Memory Atlas and Fashion Editorial.

Use only the Profiles listed in the compiled Manifest's `available_expression_profiles`.

## Deterministic text

Keep captions, dates, locations, collection names, catalogue identifiers, and source notes outside generated pixels. Add known values to each Scene Card's `metadata` object. Compile them into `presentation_contract`, bind generated images, then run `scene-card-studio present`. Omit absent metadata; never infer it.
