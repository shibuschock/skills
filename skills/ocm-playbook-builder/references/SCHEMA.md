# playbook.json + project.json — field reference

Two files drive the renderer. Claude writes both; the user never edits JSON.

## project.json (shared suite shape)

```json
{
  "project_name": "Acme ERP",
  "business_units": ["Retail", "Finance"],
  "locations": ["HQ", "Plant"],
  "brand": {
    "navy": "#162B75",
    "magenta": "#EE2C81",
    "font": "Calibri, system-ui, sans-serif",
    "footer": "Acme — Confidential"
  }
}
```

Same file the other suite skills use (cia-builder, sha-builder, comms-toolkit). Only `project_name` is required; `brand` falls back to the default palette.

## playbook.json

Top-level object with five sections: `meta`, `workstreams`, `activities`, `cadences`, `escalation`, `handoff`.

### meta

| Field | Req | Notes |
|---|---|---|
| `program_phase` | yes | e.g. "Build (MVP2)", "Deploy readiness", "Mobilization" |
| `start_reference` | yes | What Week 1 means. A real date (`"2026-07-06"`) if known, else a description (`"Week 1 = plan kickoff"`). **Never an invented date.** |
| `go_live_horizon` | no | Real go-live date(s) if known, else e.g. "~9 months out". |
| `window_weeks` | no | Length of the plan window; default 13 (≈ 90 days). |
| `team` | no | Array of `{name, role, org}` — the OCM team. |
| `version` | no | e.g. "1.0"; carry forward on refresh. |

### workstreams — array of

| Field | Req | Notes |
|---|---|---|
| `name` | yes | e.g. "Leadership & Sponsorship" (see METHODOLOGY.md for the default six). |
| `lead` | no | Named owner of the workstream. |
| `objective` | no | One sentence: what "good" looks like at day 90. |

### activities — array of

| Field | Req | Notes |
|---|---|---|
| `id` | yes | Stable short id, e.g. `"A01"`. Referenced by `depends_on`. |
| `workstream` | yes | Must match a `workstreams[].name` exactly. |
| `phase` | yes | `"30"`, `"60"`, `"90"` — or custom phase labels if the program's beats demand it (declare them consistently; the swimlane columns come from the distinct values in order of first appearance). |
| `week` | no | Integer week number relative to `start_reference` (1-based). Blank if not yet sequenced. |
| `title` | yes | Short, verb-first. |
| `description` | no | 1–3 sentences of context. |
| `owner` | yes | One named person; `"TBD"` if fully unknown; `"<Role> (name TBD)"` (e.g. `"Internal OCM Lead (name TBD)"`) when the role is known but the person isn't. The renderer flags any owner containing "TBD". Not a team name. |
| `output` | yes | The tangible artifact/event produced. |
| `done_test` | yes | How you'd verify it happened. If you can't write one, split or sharpen the activity. |
| `depends_on` | no | Array of activity `id`s that must complete first. |
| `status` | no | `"Not Started"` (default) / `"In Progress"` / `"Done"` / `"Blocked"`. |
| `linked_impacts` | no | Array of CIA `title` strings this activity mitigates — **exact match** to `cia_records.json`, that's the GAP-check contract. |

### cadences — array of

| Field | Req | Notes |
|---|---|---|
| `name` | yes | e.g. "Weekly OCM standup". |
| `frequency` | yes | e.g. "Weekly", "Biweekly (Fri)", "Monthly (last week)". |
| `audience` | no | Who attends / receives. |
| `owner` | yes | Who runs it. |
| `purpose` | no | One line. |

### escalation — array of (ordered, level 1 = lowest)

| Field | Req | Notes |
|---|---|---|
| `level` | yes | 1..n |
| `forum` | yes | e.g. "OCM Lead", "Sponsor touchpoint", "SteerCo". |
| `trigger` | yes | What sends a decision here. |
| `decision_authority` | yes | Named person/role who decides. |

### handoff — object (include only if a handoff is planned)

| Field | Req | Notes |
|---|---|---|
| `recipient` | yes | Who the plan transfers to. |
| `backup` | no | Who covers when the owner is out. |
| `items` | yes | Array of `{item, status}` — the handoff checklist (see METHODOLOGY.md §Handoff discipline for the seven standard items); `status` = "Ready" / "In Progress" / "Open". |
| `open_questions` | no | Array of strings — explicit questions needing the recipient's input. |

## Renderer behavior notes

- Derived: TBD-owner flags, activity counts per tile, GAP list (with `--cia`: CIA records with `severity >= 4` whose `title` appears in **no** activity's `linked_impacts`). Don't hand-compute these.
- Unknown `workstream` values on activities are kept but rendered in an "(Unassigned)" lane — fix the data instead.
