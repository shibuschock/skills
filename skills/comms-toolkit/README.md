# comms-toolkit

A Claude skill that turns a **change program** (ideally its **CIA**) into a running
**change-communications operation** for **any project**:

- **Comms master grid** → `<Project> Comms Master Grid.xlsx` (one row per activity)
- **Comms dashboard** → `<Project> Comms Dashboard.html` (self-contained, interactive)
- **Coverage matrix** → `<Project> Coverage Matrix.xlsx` (uncovered impacts flagged **GAP**)

The HTML dashboard is a single self-contained file (no internet/dependencies): a filterable
comms calendar, a coverage tab that highlights gaps in red, an audience × channel matrix, the
approval gate, and the crisis-comms playbook.

## How it works
Claude gathers program basics + audiences + channels + a timeline conversationally, writes
`project.json` + `comms_plan.json` itself, and runs the scripts — the user never edits JSON or
runs a terminal. See `SKILL.md`.

## Method baked in (portable change-comms)
- **Audience segmentation** — Champions / Managers / Org-wide / BU-specific / Steering Committee.
- **Channel mix + cadence** — the "What's Changing" email arc (Awareness → Process → Training),
  monthly newsletter, town halls, champion touchpoints, the **manager cascade (24h pre-brief /
  48h post-brief)**, SteerCo updates, sponsor videos, pulse surveys. Weekly beat, monthly refresh.
- **Comms-by-impact coverage** — every CIA impact maps to a vehicle; **uncovered impacts are
  flagged as GAPs** (the escalation trigger).
- **Approval / QA gate** — draft → route → reviewer SLA → send; named reviewers; factual / tone /
  scope-leak / sensitivity checks; plain-language grade 5–7.
- **Crisis comms** — activation scenarios, each with a T+24h holding, T+72h substantive, T+14d recovery.
- **ADKAR alignment** — the manager cascade drives Desire; comms map to Awareness / Desire / Knowledge.

## Layout
```
comms-toolkit/
  SKILL.md                       # instructions for Claude
  README.md                      # this file
  references/
    METHODOLOGY.md               # audiences, channels/cadence, coverage+GAP, gate, crisis, ADKAR
    SCHEMA.md                    # project.json + comms_plan.json fields
    TEMPLATES.md                 # how to use the bundled templates
  scripts/
    comms_render.py              # xlsx master grid + HTML dashboard (stdlib + openpyxl)
    coverage_matrix.py           # CIA impact x plan coverage -> GAP flags (stdlib + openpyxl)
    comms_qa.py                  # plain-language check: FK grade, long sentences, slop (stdlib)
  assets/
    templates/                   # portable Markdown drafting templates ({{placeholders}})
      email_whats_changing.md
      newsletter.md
      town_hall_faq.md
      manager_cascade.md
      steerco_update.md
      crisis_holding_statement.md
  examples/
    project.example.json         # generic "Acme ERP"
    comms_plan.example.json      # populated sample (audiences, channels, activities, coverage, gate, crisis)
```

Requires `openpyxl` for xlsx output. Python 3.9+, cross-platform (`pathlib`, `python3`). Reads
the CIA record shape from the companion **`cia-builder`** skill; audiences reconcile with
**`sha-builder`**.
