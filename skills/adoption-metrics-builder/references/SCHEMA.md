# metrics_plan.json schema

`metrics_plan.json` is a JSON object with two keys: `metrics` (array) and `measurement_plan` (object).

## `metrics[]` — one object per metric

| Field | Required | Notes |
|---|---|---|
| `id` | rec. | Short code, e.g. `E1`, `RD2`, `AD1`, `BO3`. Auto-numbered if omitted. |
| `name` | yes | Metric name, e.g. "System Login Rate". |
| `category` | yes | One of `Engagement` / `Readiness` / `Adoption` / `Business Outcome`. |
| `ladder_level` | yes | One of `Readiness Input` / `System Usage` / `Behavior/Proficiency` / `Process Outcomes` / `Business Value`. Engagement/Readiness metrics use `Readiness Input`. |
| `indicator_type` | yes | `Leading` or `Lagging`. |
| `description` | yes | What it measures and why it matters (one or two sentences). |
| `how_measured` | rec. | The calculation/method, e.g. "% of expected users logged in within 7/14/30 days". |
| `source` | yes | Concrete data source/instrument (system analytics, pulse survey, service desk, LMS, process audit...). |
| `owner` | yes | Who collects and reports it (role/team, not a person's name in generic menus). |
| `baseline` | opt. | Measured current-state value. **Blank until measured — never invented.** |
| `target` | opt. | Target value/condition. **Blank unless client-set or a defensible standard.** |
| `threshold_amber` | opt. | Value/condition at which the metric turns amber. |
| `threshold_red` | opt. | Value/condition at which the metric turns red and escalates. |
| `cadence` | rec. | Collection/reporting frequency, e.g. "Weekly during hypercare, then monthly". |
| `start_tracking` | opt. | Activation timing, e.g. "Go-live", "First pulse survey". |
| `value_levers` | opt. | Array of benefit names — must match CIA `benefits[].benefit` / record `value_levers` **exactly** for coverage matching. |
| `linked_impacts` | opt. | Array of CIA record `title`s this metric evidences — exact match required. |
| `active` | opt. | `true` if in the recommended activation set for leadership reporting. |
| `notes` | opt. | Free text (dependencies, data availability caveats). |

## `measurement_plan` — one object

| Field | Required | Notes |
|---|---|---|
| `reporting_cadence` | yes | e.g. "Monthly steering committee; weekly change-team review during hypercare". |
| `review_forum` | yes | Where metrics are reviewed and by whom. |
| `escalation` | yes | What happens on red — path and decision-maker. |
| `baseline_approach` | rec. | How/when baselines get established (e.g. first pulse survey, pre-go-live telemetry snapshot). |
| `data_collection_notes` | opt. | Instrumentation dependencies, survey waves, audit approach. |

## `project.json` (shared shape)

Same shape as the rest of the suite — see `examples/project.example.json`: `project_name`, `business_units`, optional `locations`, `phases`, and `brand` (`navy`, `magenta`, `font`, `footer`; defaults navy `#162B75`, magenta `#EE2C81`).

## Coverage matching (with `--cia`)

When rendered with `--cia cia_records.json`, the dashboard's Coverage view computes:
- **Value levers**: union of all `value_levers` across CIA records (plus `benefits[].benefit` from `project.json` if present) → any lever with no metric whose `value_levers` includes it = **GAP** (red).
- **High-severity impacts**: CIA records with `severity` ≥ 4 → any such record whose `title` appears in no metric's `linked_impacts` = **GAP** (red).

GAPs are findings, not defects to hide — do not invent metrics to zero them out; surface them to the client.
