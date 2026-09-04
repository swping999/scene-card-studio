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
| `journey-taxonomy` | Journey Taxonomy | classify visible place elements by semantic role inside one integrated spatial field |
| `street-reportage` | Street Reportage | observed public gestures, event context, and factual sequence |
| `fashion-editorial` | Fashion Editorial | pose, garment construction, movement, crop, and shot-scale rhythm |

## Expression Profiles

| Profile | Compatible systems | Expression rule |
| --- | --- | --- |
| `source-led` | all systems | derive composition, light, material, and color from the source |
| `rain-nocturne` | Cinematic Sequence | motivated rain-night light without neon excess |
| `quiet-window-light` | Quiet Editorial | plausible window light and tactile negative space |
| `watercolor-contour` | Memory Atlas | photographic anchors integrated with watercolor terrain and pencil contours |
| `watercolor-chronicle` | Memory Atlas, Family Chronicle, Museum Catalogue, Travel Journal, Journey Taxonomy | repaint every visible person, object, and place in one watercolor medium while preserving identity and geometry |
| `graphite-paper` | Family Chronicle | documentary photographs, graphite studies, paper, and supplied material evidence |
| `heritage-portrait` | Family Chronicle, Museum Catalogue | restrained silver-gelatin tonality and hand coloring without invented period identity |
| `monochrome-reportage` | Street Reportage | detailed black-and-white evidence with restrained silver-rich grain |
| `dream-logic` | Memory Atlas, Fashion Editorial | one identity-locked impossible spatial rule without random collage |
| `mineral-ink-memory` | Memory Atlas, Travel Journal, Journey Taxonomy | mineral pigment and ink organize depth and memory without historical imitation |
| `impasto-light-study` | Quiet Editorial, Memory Atlas, Travel Journal, Journey Taxonomy | thick physical paint follows one source-supported light path |
| `pixel-diary` | Memory Atlas, Travel Journal, Journey Taxonomy | rebuild the scene on one consistent hand-placed pixel grid |
| `risograph-route` | Memory Atlas, Travel Journal, Journey Taxonomy | limited inks, halftone, and overprint express source-backed route structure |
| `gouache-place-study` | Memory Atlas, Travel Journal, Journey Taxonomy | opaque matte shape groups repaint a recognizable place |
| `cyanotype-archive` | Family Chronicle, Museum Catalogue, Field Log, Street Reportage | evidence-bound Prussian-blue contact-print language without invented labels |
| `paper-relief-landscape` | Memory Atlas, Travel Journal, Journey Taxonomy | one physically coherent layered-paper landscape, not a sticker board |
| `sculpted-place-diorama` | Memory Atlas, Travel Journal, Journey Taxonomy | rebuild source geography as one physical miniature terrain model with real volume and light |
| `threaded-landscape` | Family Chronicle, Memory Atlas, Travel Journal, Journey Taxonomy | repaint the complete scene as one continuous woven, embroidered, felted, and selectively tufted textile relief |
| `autochrome-memory` | Family Chronicle, Memory Atlas, Travel Journal, Journey Taxonomy | restrained early-color photographic material without period fiction |
| `pixel-ink-memory` | Memory Atlas, Journey Taxonomy | experimental two-medium fusion: crisp near evidence, ink-wash distance |
| `travel-zine` | Memory Atlas, Family Chronicle, Travel Journal, Journey Taxonomy | restrained source-bound travel page with one memory node, sparse route evidence, and generous whitespace |
| `chinese-photo-editorial` | Quiet Editorial, Memory Atlas, Family Chronicle, Museum Catalogue | contemporary ink-and-paper photo editorial; motifs are source-supported or explicitly requested, never automatic |
| `selective-material-relief` | Memory Atlas, Family Chronicle, Travel Journal, Journey Taxonomy | real photographic subject remains intact while only the authorized environment becomes a continuous shallow relief |

`full-watercolor-memory` remains a Memory Atlas compatibility alias for `watercolor-chronicle`.

Use only the Profiles listed in the compiled Manifest's `available_expression_profiles`.
Run `scene-card-studio profiles` or `scene-card-studio profiles --system family-archive` to inspect compatible combinations before compiling.

`pixel-ink-memory` is explicitly experimental. Accept it only when pixel and ink regions share one palette, light model, composition, and depth logic; reject a split-screen or arbitrary half-and-half effect.

`travel-zine`, `chinese-photo-editorial`, and `selective-material-relief` are mechanism profiles, not generic filters. Their structured `expression_profile_tokens` in the Prompt Manifest describe composition, palette, texture, and typography decisions. Keep generated text out of pixels and apply known metadata in the deterministic presentation layer.

## Journey Taxonomy originality contract

Journey Taxonomy may use the general idea of classifying visible travel evidence, but its composition must be generated from the Scene Card. Keep one dominant place view and integrate only source-backed terrain, weather, living subjects, objects, materials, or movement cues. Do not copy a reference image's background color, duplicated overview, sticker outlines, vertical arrangement, caption position, or decorative icon set.

## Deterministic presentation

Keep captions, dates, locations, collection names, catalogue identifiers, and source notes outside generated pixels. Add known values to each Scene Card's `metadata` object. Compile them into `presentation_contract`, bind generated images, then run `scene-card-studio present`. Omit absent metadata; never infer it.

`scene-card-studio present --style journey-keepsake` is an original asymmetric collector-sheet mode. It uses one dominant generated After, a side provenance stub, and only supplied metadata. It must not reproduce a reference prompt's top/bottom comparison, 50/50 split, prescribed ticket width, sample English slogans, fringe, or decoration.
