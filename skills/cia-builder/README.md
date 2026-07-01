# cia-builder

A Claude skill that turns **raw current/future-state transcripts** into a **Change Impact Assessment** for **any project**:

- **CIA** → `<Project> CIA.xlsx` + `<Project> CIA Dashboard.html`
- a per-project **README.md**

The HTML dashboard is a single self-contained file (no internet/dependencies): filterable, sortable table; click any row for full detail; the 6 Change Dimensions shown with the Primary highlighted.

## How it works
Claude reads the transcripts and produces structured records (guided by the bundled schema + methodology); a Python script renders the xlsx + HTML. Claude gathers inputs conversationally and runs the scripts — the user never edits JSON or runs a terminal. See `SKILL.md`.

## Methodology baked in (portable OCM)
- 6 MECE **Change Dimensions** (multi-label + one **Primary**); Skills ≠ tool training.
- Severity/complexity scoring → `impact_score` and `severity_label` derived.
- **Scope** disposition (In Scope / Out of Scope / Gap).

## Optional analytical layers (appear only when your records use them)
- **TOM Shifts** — operating-model transition tiles + printable executive one-pager.
- **Value Realization** — benefits/value levers, non-monetary, with coverage and "at risk" rollups.
- **Training Needs** — modality / hours / access-constraint pivot by audience.
- **Future-State / Workshop status** — Discussed-Confirmed / Pending / Assumed + staleness flags.

## Incremental updates
Re-run on new transcripts without rebuilding: extract only the new records, merge into the existing `cia_records.json` with `scripts/cia_merge.py`, then re-render. See `references/UPDATE_LOOP.md`.

## Layout
```
cia-builder/
  SKILL.md                 # instructions for Claude
  README.md                # this file
  references/
    METHODOLOGY.md         # 6 dimensions, scoring, scope, optional layers
    CIA_SCHEMA.md          # CIA record fields (core + optional)
    UPDATE_LOOP.md         # incremental refresh from new transcripts
  scripts/
    cia_render.py          # xlsx + HTML + readme generator (stdlib + openpyxl)
    cia_merge.py           # dedup/merge new records into an existing dataset (stdlib only)
  examples/
    project.example.json
    cia_records.example.json
```

Requires `openpyxl`. Python 3.9+, cross-platform. Stakeholder analysis is the companion **`sha-builder`** skill.
