# Schema — `project.json` + `comms_plan.json`

Two small JSON files drive the toolkit. Claude writes both from the conversation; the user
never hand-edits them. See `examples/` for populated versions.

## `project.json`
Identity + branding for the program (shared shape with the other OCM skills).

| Field | Required | Notes |
|---|---|---|
| `project_name` | yes | Used to name every output file (`<Project> Comms Master Grid.xlsx`, etc.). |
| `business_units` | rec. | Array of BU names — reused as BU-specific audiences. |
| `locations` | opt. | Array of site/location names. |
| `brand` | opt. | `{navy, accent, font, footer}`. Defaults applied when omitted. |

`brand` fields: `navy` (header + xlsx headers), `accent` (channel chips), `font` (CSS font
stack), `footer` (dashboard + template footer). Hex colors like `#162B75`.

## `comms_plan.json`
The operating plan. A JSON object with these keys:

### `audiences` — `[{id, name, description}]`
The segments (Champions / Managers / Org-wide / BU-specific / Steering Committee, or your own).
`id` is referenced by `activities[].audience` and `coverage[].audience`; the renderer resolves
ids back to `name` for display. `name` should match SHA stakeholder-group names.

### `channels` — `[{name, cadence, owner}]`
The vehicle catalog. `cadence` e.g. "Weekly" / "Monthly" / "Per milestone"; `owner` is the
accountable role. Reference is by `name` from `activities[].channel`.

### `activities` — `[{week, date, audience, channel, title, owner, comm_ref, review_gate, status}]`
One row per scheduled comm. This is the master grid and the calendar table.

| Field | Notes |
|---|---|
| `week` | Integer week number (sequencing beat). |
| `date` | Send/run date (`YYYY-MM-DD`). If the program has no calendar anchor (only relative milestones like "Month 6"), agree a week-1 anchor date with the user; otherwise use week numbers in titles and a placeholder ISO date noted as a placeholder — never silently invent real dates. |
| `audience` | An `audiences[].id` or name. |
| `channel` | A `channels[].name`. |
| `title` | The activity (e.g. "What's Changing Ep.1 — Awareness"). |
| `owner` | Accountable person/role. |
| `comm_ref` | Short tracking code (e.g. `WC-01`). |
| `review_gate` | Where it stands in the gate ("Not started" / "In review" / "Approved" / "n/a"). |
| `status` | Delivery status: `Planned` / `Draft` / `Approved` / `Sent`. Defaults to `Planned`. |

### `coverage` — `[{impact, impact_id, vehicle, audience, status}]`
Maps CIA impacts to the vehicle(s) that carry them.

| Field | Notes |
|---|---|
| `impact` | CIA impact title (match to CIA `title`). |
| `impact_id` | CIA 1-based id (position in `cia_records.json`). Either `impact` or `impact_id` lets `coverage_matrix.py` match. |
| `vehicle` | The comm(s) that cover it. |
| `audience` | An `audiences[].id` or name. |
| `status` | `covered` or `gap`. `gap` = tracked, intended-but-not-yet-built coverage (renders red). |

### `approval_gate` — `{draft_by, route, sla_hours, reviewers[], send}`

| Field | Notes |
|---|---|
| `draft_by` | Role that drafts. |
| `route` | The routing chain (e.g. "Comms Lead -> Change Lead -> Sponsor"). |
| `sla_hours` | Reviewer turnaround SLA (e.g. 48). |
| `reviewers` | Array of named reviewers + what they check (factual / tone / scope-leak / sensitivity). |
| `send` | Role that sends after sign-off. |

### `crisis` — `[{scenario, holding_24h, substantive_72h, recovery_14d}]`
Pre-agreed crisis playbooks.

| Field | Notes |
|---|---|
| `scenario` | Trigger (e.g. "Vendor / partner delay", "Data incident", "Exec departure"). |
| `holding_24h` | T+24h holding statement. |
| `substantive_72h` | T+72h substantive update. |
| `recovery_14d` | T+14d recovery message. |

## Outputs (derived — do not hand-build)
- `comms_render.py` → `<Project> Comms Master Grid.xlsx` + `<Project> Comms Dashboard.html`.
- `coverage_matrix.py` → `<Project> Coverage Matrix.xlsx` (uncovered impacts flagged **GAP**).
- `comms_qa.py` → console report (Flesch-Kincaid grade, long sentences, slop terms).
