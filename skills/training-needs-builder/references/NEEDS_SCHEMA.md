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
| `phase` | opt. | The program phase/wave the need belongs to, taken from the project's canonical scope-by-phase source. Omit when the program has no phases. |
| `phase_basis` | rec. if `phase` | The source document and the reason for the phase (who or what says so, with its date). |
| `phase_unverified` | opt. | `true` when the canonical source does not cover this need and the phase is a best reading. Renders as a "phase unverified" flag. |
| `process_l2` / `function_l1` | opt. | Process-taxonomy labels, when the program has a process hierarchy. |
| `capability_basis` | opt. | How the capability statement was derived (e.g. "CIA role_changes evidence" or a rewrite note). |
| `gap_basis` | opt. | Why the gap size was set (e.g. "sized from max CIA severity", or "assumed, pending confirmation"). |
| `population_basis` | opt. | Where the headcount came from and how the audience name was matched to it. |
| `role_change_inferred` / `role_change_inferred_source` | opt. | Use when the CIA lists the audience but states no change for it. The text is the inferred change; the source field says how it was inferred. Never present an inferred change as a stated one. |
| `reviewed` | opt. | `false` by default. A functional-reviewer confirmation flag — set when a person has actually looked at this need, independent of whether they changed anything. Distinct from an adjustment: it's a "checked" signal, not a data correction. When the dashboard exposes an editable review layer, track it the same way as other reviewer edits (local override, diffed against baseline, included in the feedback tracker payload) rather than writing straight back to this file. |

**Derived / don't hand-compute downstream:** module groupings, learning paths, schedule — those belong to curriculum/rollout.

`business_unit` and `audience` may be a string or a list; the renderer joins lists with " / ".

## Dispositions (impact coverage)
Every CIA impact must land somewhere. Impacts that yield **no trainable need** go in a sibling file, `needs_dispositions.json` — a JSON array of `{ "impact": "<CIA id or title>", "disposition": "no-need" | "deferred", "reason": "…" }`. This makes impact→need coverage machine-checkable: every CIA impact appears either in some need's `source_impacts` or in `needs_dispositions.json`.

## Linkage
`source_impacts` ties each need back to the CIA. Downstream, curriculum modules reference these capabilities via `maps_to_needs`, preserving the thread: **impact → need → module → wave**.
