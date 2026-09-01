# Scene Card schema

Keep evidence and interpretation separate.

## Source fields

| Field | Meaning |
| --- | --- |
| `source` | Local photo path; never replace with a guessed URL |
| `width`, `height` | Native dimensions |
| `palette` | Three to five source-derived colors |
| `brightness`, `saturation` | Normalized values from 0 to 1 |
| `orientation` | `portrait`, `landscape`, or `square` |
| `caption` | Short concrete line, not invented metadata |

## Observation

Only record visibly supported information:

- `subjects`: primary visible subjects;
- `dominant_gesture`: main direction, movement, or stable axis;
- `quiet_regions`: low-information regions safe for breathing room or text.

## Interpretation

Record tentative, editable meaning separately from visible evidence:

- `narrative_intent`: concise purpose such as `departure` or `family continuity`;
- `emotional_tone`: one to three restrained descriptors;
- `confidence`: normalized confidence from 0 to 1;
- `method`: `heuristic`, `user-directed`, or another honest method label.

## Direction

Record editable presentation decisions:

- `story_role`: `moment` for a standalone photo; `opening`, `development`, `pause`, or `closing` for a sequence;
- `director_note`: state how to treat the frame and what cliché to avoid;
- `layout_emphasis`: the subject, gesture, relationship, or quiet region the layout should prioritize.

Preserve user chronology when dates or order carry meaning. Without chronology, open with a legible establishing frame, develop through contrast, use the quietest frame as a pause, and close with resolution or an intentional open ending.

## Presentation readiness

Low-level local analysis does not identify semantic content. Before presentation synthesis, every Scene Card must contain non-placeholder values for:

- `observation.subjects` and `observation.dominant_gesture`;
- `interpretation.narrative_intent`;
- `direction.director_note` and `direction.layout_emphasis`;
- `transformation.must_preserve` and `transformation.may_transform`.

Use `scene-card-studio check story.json --json`. Missing fields must stop cloud consent and generation; never fill them by guessing hidden content.
