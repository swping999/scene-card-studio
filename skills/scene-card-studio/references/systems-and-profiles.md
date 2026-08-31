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

| Profile | Compatible systems | Expression rule |
| --- | --- | --- |
| `source-led` | all systems | derive composition, light, material, and color from the source |
| `rain-nocturne` | Cinematic Sequence | motivated rain-night light without neon excess |
| `quiet-window-light` | Quiet Editorial | plausible window light and tactile negative space |
| `watercolor-contour` | Memory Atlas | photographic anchors integrated with watercolor terrain and pencil contours |
| `watercolor-chronicle` | Memory Atlas, Family Chronicle, Museum Catalogue, Travel Journal | repaint every visible person, object, and place in one watercolor medium while preserving identity and geometry |
| `graphite-paper` | Family Chronicle | documentary photographs, graphite studies, paper, and supplied material evidence |
| `heritage-portrait` | Family Chronicle, Museum Catalogue | restrained silver-gelatin tonality and hand coloring without invented period identity |
| `monochrome-reportage` | Street Reportage | detailed black-and-white evidence with restrained silver-rich grain |
| `dream-logic` | Memory Atlas, Fashion Editorial | one identity-locked impossible spatial rule without random collage |

`full-watercolor-memory` remains a Memory Atlas compatibility alias for `watercolor-chronicle`.

Use only the Profiles listed in the compiled Manifest's `available_expression_profiles`.
Run `scene-card-studio profiles` or `scene-card-studio profiles --system family-archive` to inspect compatible combinations before compiling.

## Deterministic text

Keep captions, dates, locations, collection names, catalogue identifiers, and source notes outside generated pixels. Add known values to each Scene Card's `metadata` object. Compile them into `presentation_contract`, bind generated images, then run `scene-card-studio present`. Omit absent metadata; never infer it.
