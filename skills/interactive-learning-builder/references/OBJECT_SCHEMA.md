# Learning object schema

`learning_object.json` defines one interactive object. The render script (`scripts/render_object.py`) turns it into self-contained HTML.

## Common fields
| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable slug (used as filename + SCORM id + flashcard localStorage key). e.g. `pos-refunds-quiz`. |
| `title` | yes | Learner-facing title. |
| `format` | yes | `"quiz"` or `"flashcards"`. |
| `audience` | opt. | Shown as "For: …". |
| `module_ref` | opt. | Curriculum module id this maps to (traceability). |
| `objectives` | opt. | Array of objective strings; shown on the results screen. |
| `items` | yes | Array — shape depends on `format` (below). |

## format: "quiz"
Extra field: `pass_threshold` (0–1, default `0.8`).

Each item:
| Field | Required | Notes |
|---|---|---|
| `type` | opt. | `"single"` (default) or `"multiple"` (select-all-that-apply). |
| `question` | yes | The stem. Frame at the right Bloom level (Apply = a task/situation, not recall). |
| `bloom` | opt. | Shown as a small tag (e.g. "Apply"). |
| `options` | yes | Array of `{ "text": "...", "correct": true|false, "feedback": "..." }`. `feedback` is per-option (best for single-select). |
| `feedback_correct` / `feedback_incorrect` | opt. | Fallback feedback when an option has none. |

## format: "flashcards"
Each item:
| Field | Required | Notes |
|---|---|---|
| `front` | yes | Prompt side. |
| `back` | yes | Answer side. |
| `hint` | opt. | Shown on the front. |

Flashcards use spaced-repetition-lite: the learner rates each card "Got it" / "Needs review"; ratings persist in the browser (`localStorage`, keyed by `id`) so review cards surface first next time.

## Authoring rules
- Match each question's verb/difficulty to the module objective it measures.
- Prefer scenario/task questions over trivia for skill objectives — completion ≠ competence.
- Write feedback that *teaches* (why it's right/wrong), not just "Correct/Incorrect".
- Don't fabricate system screen/field specifics — use `[CONFIRM: …]` placeholders for SME review.
- Keep learner language short and plain (American English).
