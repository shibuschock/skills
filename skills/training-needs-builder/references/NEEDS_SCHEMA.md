# Training needs schema

`training_needs.json` is a JSON array. One object per **audience × capability** (a thing a role must be able to do that they can't today). Fields:

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable need id, `TN-01`, `TN-02`, … Downstream modules reference needs by this id via `maps_to_needs`. |
| `capability` | yes | Verb-led, observable: what the learner must be able to DO (e.g. "Process a refund with manager override in the POS"). Not "understand the POS". |
| `audience` | yes | Role/persona. Reconcile to the project context file's audiences AND the CIA `roles_impacted` (CIA is canonical). |
| `business_unit` | yes | From the project context file (e.g. Retail / Finance / Supply Chain). |
| `source_impacts` | yes | Array of CIA `id` or `title` values this need derives from. The traceability link. |
| `driver_dimensions` | rec. | Subset of the 6 CIA Change Dimensions driving the need. Copy from the impact(s). |
| `current_proficiency` | rec. | Novice / Advanced Beginner / Competent / Proficient / Expert. Blank if unknown. |
| `target_proficiency` | yes | Same scale. Default Competent (frontline) / Proficient (leads, super-users). |
| `gap` | derived | Qualitative size of current→target (Small / Moderate / Large). |
| `bloom_level` | rec. | Remember / Understand / Apply / Analyze / Evaluate / Create. Usually Apply for system tasks. |
| `priority` | yes | Critical / High / Medium / Low. Inherit from CIA `priority` if present, or derive from `impact_score` (severity × complexity) if those fields exist. **If the CIA carries neither** (common), derive from qualitative signals — compliance exposure, go-live criticality, population size — and record the basis in `notes`. |
| `recommended_modalities` | rec. | Array from the modality catalog. Seed from CIA `training_modality` + the impact→response map. |
| `estimated_hours` | opt. | Per learner. Carry from CIA `estimated_training_hours` if the CIA has it; blank if unknown — never derive hours here. |
| `population_size` | opt. | Headcount in this audience. PLACEHOLDER + flag if unknown. |
| `access_constraints` | opt. | Device/time/language/location limits. Carry from CIA `access_constraints`. |
| `training_alone_insufficient` | opt. | `true` when Mindset/Culture or Role/Accountability is the impact's PRIMARY dimension, or when the impact's mitigation text names a non-training response. A secondary Mindset dimension alone → note it, don't flag. |
| `non_training_response` | opt. | When the flag above is true: the coaching/comms/role-definition response needed instead of (or alongside) a course. |
| `notes` | opt. | Anything else (super-user need, prerequisite, sequencing hint). |

**Derived / don't hand-compute downstream:** module groupings, learning paths, schedule — those belong to curriculum/rollout.

## Dispositions (impact coverage)
Every CIA impact must land somewhere. Impacts that yield **no trainable need** go in a sibling file, `needs_dispositions.json` — a JSON array of `{ "impact": "<CIA id or title>", "disposition": "no-need" | "deferred", "reason": "…" }`. This makes impact→need coverage machine-checkable: every CIA impact appears either in some need's `source_impacts` or in `needs_dispositions.json`.

## Linkage
`source_impacts` ties each need back to the CIA. Downstream, curriculum modules reference these capabilities via `maps_to_needs`, preserving the thread: **impact → need → module → wave**.
