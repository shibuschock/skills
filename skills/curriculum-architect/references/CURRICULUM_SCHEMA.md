# Curriculum schema

`curriculum.json` is a JSON object with three keys: `learning_paths`, `modules`, `assessment_plan`.

## `learning_paths` — array
One per audience (or audience cluster).

| Field | Required | Notes |
|---|---|---|
| `path_name` | yes | e.g. "Frontline — Go-Live Ready". |
| `audience` | yes | Matches a needs `audience` / context audience. |
| `business_unit` | yes | From the project context file (e.g. Retail / Finance / Supply Chain). |
| `sequence` | yes | Ordered array of module `id`s. |
| `total_hours` | derived | Sum of module durations; sanity-check vs `access_constraints`. |
| `target_proficiency` | rec. | The path's overall destination (Competent / Proficient). |

## `modules` — array

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable slug, e.g. `pos-refunds-01`. |
| `title` | yes | Learner-facing. |
| `audience` | yes | Who it's for. |
| `learning_objectives` | yes | Array of `{ "text": "By the end, the learner can …", "bloom_level": "Apply", "capability_ref": "TN-01" }`. `capability_ref` is the **need id** (`TN-xx`) the objective satisfies — not the full capability string. Observable + measurable. |
| `duration_minutes` | yes | Realistic for the audience/modality. Covers the **formal band only** (scheduled facilitated time, incl. hands-on labs); experiential/social bands are estimated separately or left unsized. |
| `modality_blend` | yes | `{ "experiential": "...", "social": "...", "formal": "..." }` — name what happens in each 70-20-10 band, not just %s. |
| `blend_weights` | opt. | `{ "experiential": 40, "social": 45, "formal": 15 }` — the module's ACTUAL blend proportions when they shift from the 70-20-10 default (e.g. coaching-led modules for mindset/role needs). Omit to use the default (the renderer then labels the bar "default blend"). |
| `non_training_gates` | opt. | Array of strings — non-training preconditions carried from the TNA's `non_training_response` (policy decision, role redesign, sponsor action, negotiated commitment). Rendered as amber chips; the gates travel to rollout. |
| `status` | opt. | `"planned"` (default) or `"gated — do not build"` with a `gate` string giving the reason. Gated modules render distinctly and must not be built or scheduled until the gate clears. |
| `prerequisites` | rec. | Array of module `id`s that must come first. |
| `content_outline` | rec. | High-level section list (detailed build = content-builder). |
| `assessment` | yes | `{ "type": "task check | scenario | quiz | observation", "mastery_threshold": "...", "kirkpatrick_level": "L2" }`. |
| `maps_to_needs` | yes | Array of need `id`s (`TN-01`, …) this module delivers. |
| `maps_to_impacts` | rec. | Array of CIA `id`/`title` (carried through from the needs). Preserves traceability. |
| `super_user_track` | opt. | `true` if this is the deeper champion/super-user version. |

## `assessment_plan` — object
Program-level view.

| Field | Notes |
|---|---|
| `approach` | Backward-design summary: objectives → assessments → content. |
| `levels` | Which Kirkpatrick levels are measured where (L1 reaction, L2 learning, L3 behavior, L4 results). |
| `mastery_policy` | e.g. "Frontline must pass the task check before floor access." |
| `ties_to_value` | Link L4 to CIA `value_levers` so learning measurement connects to value realization. |

## Rules
- **Backward design**: objective → assessment → content. Never list content with no objective.
- Bloom verb must match the proficiency target (Apply for most frontline tasks; Analyze/Evaluate for judgment roles).
- Every module traces to ≥1 need; the thread **impact → need → module** stays unbroken.
- Every need flagged `training_alone_insufficient` carries its gates into some module's `non_training_gates` (or a gated placeholder module) — the flag must not be lost between TNA and rollout.
