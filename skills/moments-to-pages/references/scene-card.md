# Scene Card schema

Create one JSON object per photograph:

| Field | Meaning |
| --- | --- |
| `source` | Local photo path; never replace it with a guessed URL |
| `width`, `height` | Native dimensions |
| `palette` | Three to five source-derived hex colors |
| `brightness`, `saturation` | Normalized values from 0 to 1 |
| `orientation` | `portrait`, `landscape`, or `square` |
| `story_role` | `opening`, `development`, `pause`, or `closing` |
| `caption` | Short concrete line, not invented metadata |
| `subjects` | Visible primary subjects only |
| `dominant_gesture` | Main direction, movement, or stable axis |
| `quiet_regions` | Low-information regions safe for breathing room or text |

Preserve user-supplied chronology when dates or order carry meaning. Without chronology, open with a legible establishing frame, develop through visual or semantic contrast, place the quietest frame as a pause, and close with resolution or an intentional open ending.
