# CIA record schema

`cia_records.json` is a JSON array. One object per **change impact** (a current→future change to how people work). Fields:

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Short name of the change (verb-led, e.g. "Automated replenishment replacing manual reorder"). |
| `functional_area` | yes | The workshop/design area this came from (e.g. "Retail Operations"). |
| `business_unit` | yes | BU from `project.json` (e.g. "Retail"). |
| `l1_process` / `l2_process` / `l3_process` | rec. | Process hierarchy. L2 is the main grouping; L1/L3 optional. |
| `current_state` | yes | How it works today (from the *current-state* transcript). |
| `future_state` | yes | How it will work (from the *future-state* transcript). |
| `process_change` | yes | One-sentence summary of the shift. |
| `roles_impacted` | yes | Comma/semicolon list of roles affected. |
| `role_changes` | opt. | Object `{ "Role": {"desc": "...", "evidence": "workshop"} }` or `{ "Role": "desc" }` — per-role responsibility delta. |
| `severity` | rec. | 1–5 (magnitude for affected roles). Leave blank if unscored. |
| `complexity` | rec. | 1–5 (how hard the change is). |
| `priority` | rec. | Critical / High / Medium / Low. |
| `sentiment` | opt. | Positive / Mixed / Neutral / Negative / Cautious. |
| `change_considerations` | rec. | Adoption friction + a source-attributed quote if available. |
| `mitigation` | rec. | Response: "Training (...), Communication (...), Coaching (...)". |
| `dimensions` | yes | Array of the dimensions that **materially** apply (subset of the 6 — see METHODOLOGY.md). |
| `primary_dimension` | yes | Exactly one, the load-bearing dimension (must be in `dimensions`). |
| `scope` | opt. | `In Scope` (default) / `Out of Scope - Adjacent` / `Gap - Requirement Unconfirmed`. |

**Derived automatically** (do NOT supply): `id`, `severity_label`, `impact_score` (= complexity × severity), primary-first dimension ordering, `stale` (from `last_reviewed`).

The 6 dimensions (exact strings): `Role/Accountability`, `Process/Policy`, `Ways of Working`, `Data/Decision Inputs`, `Skills/Capability`, `Mindset/Culture`.

## Optional analytical fields

All optional. Populate **only when the transcript supports it** — a blank is correct, an invented value is a defect. The dashboard grows an extra tab for each layer only when at least one record carries its field(s).

| Field | Feeds | Notes |
|---|---|---|
| `future_state_status` | status ribbon, Workshop Status, Value Realization | One of `Discussed-Confirmed` / `Discussed-Pending` / `Assumed`. If omitted, it's inferred: `Discussed-Pending` when `workshop_reference`/`evidence_source` is present, else `Assumed`. |
| `evidence_source` | detail, status inference | Free text + link: where the future state was established. |
| `workshop_reference` | Workshop Status, status inference | Workshop date + filename/title. |
| `last_reviewed` | Workshop Status (staleness) | Date (`YYYY-MM-DD`). Rows older than `training.stale_days` (default 30) flag as stale. |
| `tom_shift` | TOM Shifts tab | Single label naming the target-operating-model transition this impact belongs to. Match a `tom_shifts[].name` in `project.json` to get a tile description + today/future + one-pager. |
| `value_levers` | Value Realization tab | Array of benefit names. Match `benefits[].benefit` in `project.json` for descriptions + zero-coverage flags. |
| `benefit_at_risk` | detail | Free text — what value is unrealized if adoption fails. |
| `training_modality` | Training Needs tab | Array, e.g. `["ILT","VILT","e-learning","in-app guidance","job aid","coaching"]`. |
| `estimated_training_hours` | Training Needs tab | Number per learner; blank where unknown. |
| `access_constraints` | detail | Free text (device, scheduled time, language, location). |

"At risk" on the Value Realization tab is derived: mapped impacts where `sentiment` ∈ {Mixed, Negative} **and** `complexity` ≥ 4.

See `examples/cia_records.example.json` (shows both core and optional fields) and `references/UPDATE_LOOP.md` for the incremental refresh workflow.
